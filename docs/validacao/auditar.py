"""Auditoria agregada da coleta preservada, independente das transformações do painel."""
import argparse
import csv
import hashlib
import math
import re
import struct
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from statistics import mean, median

p = argparse.ArgumentParser(description=__doc__)
for arg in ("versao", "coleta", "saida"):
    p.add_argument(arg, type=Path)
p.add_argument("--conversor", type=Path, help="Executável local alternativo que recebe origem e destino")
a = p.parse_args()
sys.path.insert(0, str(a.versao / "processamento"))
from leitor_dbf import registros

def ler(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def escrever(nome, rows):
    with (a.saida / (nome + ".csv")).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0])
        w.writeheader()
        w.writerows(rows)

def duplicadas(db):
    with db.open("rb") as f:
        n, start, width = struct.unpack_from("<IHH", f.read(32), 4)
        f.seek(start)
        seen = set()
        repeats = 0
        for _ in range(n):
            row = f.read(width)
            if len(row) != width:
                raise ValueError("Registro truncado")
            if row[:1] == b" ":
                repeats += row in seen
                seen.add(row)
        return repeats

def inteiro(s):
    if not s:
        return None
    d = Decimal(s)
    if d < 0 or d != int(d):
        raise ValueError("Quantidade inválida")
    return int(d)

def soma(values):
    return sum(values) if values and None not in values else None

def quantil(values, q):
    idx = (len(values)-1)*q
    lo = int(idx)
    return values[lo] + (values[math.ceil(idx)]-values[lo])*(idx-lo)

manifesto = ler(a.versao / "processamento/manifesto_publico.csv")
painel = ler(a.versao / "dados/painel.csv")
ref = {(r["competencia"],r["CNES"]): r for r in painel}
if len(ref) != len(painel):
    raise ValueError("Chave repetida no painel")
meses = sorted({r["competencia"] for r in manifesto})
esperados = {f"{ano}{mes:02}" for ano, meses_ano in [(2025,range(6,13)),(2026,range(1,7))] for mes in meses_ano}
if set(meses) != esperados:
    raise ValueError("Competências inesperadas")
a.saida.mkdir(parents=True, exist_ok=False)
rd_out, repet, lt_out, valid = [], [], [], []
def conferir(m, k, campo, esperado):
    bruto = ref.get((m,k),{}).get(campo)
    obs = None if bruto in ("",None) else float(bruto)
    ok = (m,k) in ref and ((obs is None and esperado is None) or
          (obs is not None and esperado is not None and math.isclose(obs,esperado,rel_tol=0,abs_tol=1e-8)))
    valid.append(dict(competencia=m,CNES=k,indicador=campo,referencia_DBF=esperado,painel=bruto,situacao="confere" if ok else "diverge"))

with tempfile.TemporaryDirectory() as td:
    for m in meses:
        arqs = {}
        for base in ("RD","LT"):
            item, = [r for r in manifesto if r["competencia"]==m and r["base"]==base]
            src, = a.coleta.rglob(item["arquivo"])
            if hashlib.sha256(src.read_bytes()).hexdigest()!=item["sha256"]:
                raise ValueError("SHA-256 divergente em " + src.name)
            db = Path(td) / (src.stem+".dbf")
            if a.conversor:
                subprocess.run([str(a.conversor),str(src),str(db)],check=True)
            else:
                from pyreaddbc import dbc2dbf
                dbc2dbf(str(src),str(db))
            arqs[base]=db
        rd = defaultdict(list)
        ids = defaultdict(list)
        tipos = Counter()
        for r in registros(arqs["RD"],"CNES ANO_CMPT MES_CMPT MUNIC_MOV N_AIH IDENT DIAS_PERM VAL_TOT".split()):
            k,t,ident = r["CNES"].zfill(7),r["IDENT"],r["N_AIH"]
            if not (re.fullmatch(r"[0-9]{1,7}",r["CNES"]) and int(k) and re.fullmatch(r"[0-9]{1,13}",ident) and
                    r["ANO_CMPT"]+r["MES_CMPT"].zfill(2)==m and re.fullmatch(r"53[0-9]{4}",r["MUNIC_MOV"]) and t in ("1","5")):
                raise ValueError("Elegibilidade RD a investigar em "+m)
            v = inteiro(str(Decimal(r["VAL_TOT"])*100)) if r["VAL_TOT"] else None
            rd[k].append((t,inteiro(r["DIAS_PERM"]),v,ident.zfill(13)))
            ids[ident.zfill(13)].append((t,k))
            tipos[t]+=1
        dups = duplicadas(arqs["RD"])
        rd_out.append(dict(competencia=m,linhas=sum(tipos.values()),IDENT_1=tipos["1"],IDENT_5=tipos["5"],IDs_distintos_no_mes=len(ids),linhas_excedentes=sum(tipos.values())-len(ids),linhas_identicas_bytes_DBF=dups,invalidos_chave_tipo_territorio=0))
        grupos=Counter((len(v),sum(t=="1" for t,k in v),sum(t=="5" for t,k in v),len({k for t,k in v})) for v in ids.values() if len(v)>1)
        for (n,normal,pror,hosp),n_grupos in sorted(grupos.items()):
            repet.append(dict(competencia=m,ocorrencias_por_grupo=n,normais=normal,prorrogacoes=pror,CNES_distintos=hosp,quantidade_de_grupos=n_grupos))
        leitos=defaultdict(list)
        cats=defaultdict(list)
        keys=Counter()
        for r in registros(arqs["LT"],"CNES COMPETEN CODUFMUN TP_LEITO CODLEITO QT_EXIST QT_SUS".split()):
            k=r["CNES"].zfill(7)
            if r["COMPETEN"]!=m or not r["CODUFMUN"].startswith("53"):
                raise ValueError("Território/competência LT a investigar")
            cat=(r["TP_LEITO"].zfill(2),r["CODLEITO"].zfill(2))
            par=(inteiro(r["QT_EXIST"]),inteiro(r["QT_SUS"]))
            keys[(k,*cat)]+=1
            leitos[k].append(par)
            cats[cat].append(par)
        for cat,ls in sorted(cats.items()):
            lt_out.append(dict(competencia=m,TP_LEITO=cat[0],CODLEITO=cat[1],linhas=len(ls),QT_EXIST=soma([x for x,y in ls]),QT_SUS=soma([y for x,y in ls]),chaves_excedentes=sum(n-1 for (k,t,c),n in keys.items() if (t,c)==cat),sus_maior_exist=sum(x is not None and y is not None and y>x for x,y in ls)))
        for k,rows in rd.items():
            dias=[d for t,d,v,i in rows if t=="1"]
            ds=sorted(d for d in dias if d is not None)
            completo=bool(ds) and len(ds)==len(dias)
            b=leitos[k]
            sus=soma([y for x,y in b])
            vals=dict(aih_registros=len(rows),aih_normais=len(dias),aih_prorrogacao=len(rows)-len(dias),numeros_aih_distintos=len({i for t,d,v,i in rows}),valor_total_centavos=soma([v for t,d,v,i in rows]),leitos_sus=sus,leitos_existentes=soma([x for x,y in b]),dias_normais_total=soma(dias),n_permanencia_valida=len(ds),n_permanencia_ausente=len(dias)-len(ds),permanencia_media=mean(ds) if completo else None,permanencia_mediana=median(ds) if completo else None,permanencia_q1=quantil(ds,.25) if completo else None,permanencia_q3=quantil(ds,.75) if completo else None,aih_por_leito_sus=len(rows)/sus if sus else None)
            vals["valor_medio_reais"]=vals["valor_total_centavos"]/100/len(rows) if vals["valor_total_centavos"] is not None else None
            for campo,valor in vals.items():
                conferir(m,k,campo,valor)
        if set(rd)!={k for mes,k in ref if mes==m}:
            raise ValueError("Cobertura por chave divergente em "+m)
        print("Competência conferida:",m,flush=True)
for nome,rows in [("auditoria_elegibilidade_rd",rd_out),("analise_repeticoes_aih",repet),("auditoria_leitos",lt_out),("validacao_indicadores",valid)]:
    escrever(nome,rows)
falhas=sum(x["situacao"]!="confere" for x in valid)+sum(x["linhas_identicas_bytes_DBF"] for x in rd_out)+sum(x["chaves_excedentes"]+x["sus_maior_exist"] for x in lt_out)
print("Comparações:",len(valid),"Divergências ou exceções de integridade:",falhas)
sys.exit(int(bool(falhas)))
