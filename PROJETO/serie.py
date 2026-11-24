"""Aquisição retomável da série RD, ST e LT do DF, com biblioteca padrão."""
import argparse
import concurrent.futures
import csv
import getpass
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import shutil
import sys
import tempfile
from urllib.request import urlopen

BRASILIA = timezone(timedelta(hours=-3))
MESES = [f"2025{m:02}" for m in range(6, 13)] + [f"2026{m:02}" for m in range(1, 7)]
PASTAS = {"RD": "SIHSUS/200801_/Dados", "ST": "CNES/200508_/Dados/ST", "LT": "CNES/200508_/Dados/LT"}

def hash_arquivo(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

def salvar(path, registro):
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False, mode="w", encoding="utf8") as tmp:
        json.dump(registro, tmp, ensure_ascii=False, indent=2)
    Path(tmp.name).replace(path)

def obter(base, competencia, tipo, responsavel, timeout):
    pasta = base / competencia
    pasta.mkdir(exist_ok=True, parents=True)
    nome = f"{tipo}DF{competencia[2:]}.dbc"
    arquivo = pasta / nome
    ficha = pasta / (nome + ".json")
    if ficha.exists():
        anterior = json.loads(ficha.read_text(encoding="utf8"))
        if anterior["status"] == "obtido":
            if arquivo.is_file() and hash_arquivo(arquivo) == anterior["sha256"]:
                return anterior
            raise ValueError(f"Original alterado: {arquivo}. Preserve a pasta e use outro destino.")
    url = f"ftp://ftp.datasus.gov.br/dissemin/publicos/{PASTAS[tipo]}/{nome}"
    r = dict(id=nome[:-4],base=tipo,uf="DF",competencia=competencia,arquivo=nome,url=url,
             tentativa=datetime.now(BRASILIA).isoformat(),responsavel=responsavel,
             download="",bytes="",sha256="",layout="",link_drive="",erro="")
    tmp = None
    try:
        with urlopen(url, timeout=timeout) as resposta, tempfile.NamedTemporaryFile(dir=pasta,delete=False) as saida:
            tmp = Path(saida.name)
            shutil.copyfileobj(resposta, saida)
            r["url"] = resposta.geturl()
        with tmp.open("rb") as data:
            header = data.read(32)
        if len(header) < 32 or header[0] not in (3, 131) or int.from_bytes(header[8:10],"little") < 33:
            raise ValueError("Cabeçalho incompatível com o DBC esperado")
        if arquivo.exists() and hash_arquivo(tmp) != hash_arquivo(arquivo):
            raise ValueError("Destino já contém conteúdo diferente")
        r.update(bytes=tmp.stat().st_size,sha256=hash_arquivo(tmp),download=datetime.now(BRASILIA).isoformat(),status="obtido")
        tmp.replace(arquivo)
    except (OSError, ValueError) as exc:
        r.update(status="falha",erro=str(exc))
    finally:
        if tmp and tmp.exists():
            tmp.unlink()
    salvar(ficha,r)
    return r

def executar(base, responsavel, timeout):
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        tarefas=[pool.submit(obter,base,m,t,responsavel,timeout) for m in MESES for t in PASTAS]
        linhas=[t.result() for t in tarefas]
    with (base/"manifesto.csv").open("w",encoding="utf-8-sig",newline="") as stream:
        w=csv.DictWriter(stream,fieldnames=list(linhas[0]),delimiter=";")
        w.writeheader()
        w.writerows(linhas)
    return sum(r["status"]=="obtido" for r in linhas)

def processar(base):
    from tccbi.pipeline import ingest, profile, prepare_all, build, read_json, write_json
    for m in MESES:
        fichas=[read_json(base/m/f"{t}DF{m[2:]}.dbc.json") for t in PASTAS]
        if any(f["status"]!="obtido" for f in fichas):
            raise ValueError(f"Aquisição incompleta em {m}")
        run=base/"execucoes"/m
        for f in fichas:
            if hash_arquivo(base/m/f["arquivo"])!=f["sha256"]:
                raise ValueError(f"Conteúdo divergente: {f['arquivo']}")
        if not run.exists():
            ingest(run,m,base/m)
        manifest=read_json(run/"manifesto.json")
        for f in fichas:
            item=manifest["arquivos"][f["base"]]
            if item["sha256"]!=f["sha256"]:
                raise ValueError(f"Versão divergente: {m}")
            item["aquisicao_oficial"]=f
        write_json(run/"manifesto.json",manifest)
        profile(run)
        prepare_all(run)
        build(run)

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("acao",choices=["baixar","processar"])
    p.add_argument("--destino",type=Path,default=Path("coleta_df"))
    p.add_argument("--responsavel",default=getpass.getuser())
    p.add_argument("--timeout",type=int,default=45)
    args=p.parse_args()
    if args.acao=="baixar":
        n=executar(args.destino,args.responsavel,args.timeout)
        print(f"{n}/39 arquivos obtidos. Manifesto: {args.destino/'manifesto.csv'}")
        sys.exit(0 if n==39 else 1)
    processar(args.destino)
