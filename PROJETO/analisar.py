"""Execute com o Python do protótipo, informando sua pasta como argumento."""
import hashlib
import json
import struct
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

raiz = Path(sys.argv[1]).resolve()
saida = Path(__file__).resolve().parent
sys.path[:0] = [str(saida / ".dependencias"), str(raiz)]
import pandas as pd
from pyreaddbc import dbc2dbf
from serie import MESES, PASTAS, hash_arquivo
from scripts.conferir_dbf import registros
from tccbi.core import REQUIRED, prepare, integrate, pilot
from tccbi.auditoria import conferir_chaves


def salvar(dados, nome):
    pd.DataFrame(dados).to_csv(saida / nome, index=False, encoding="utf-8-sig")


def ler_dbc(origem, tipo, pasta):
    dbf = pasta / (tipo + ".dbf")
    dbc2dbf(str(origem), str(dbf))
    with origem.open("rb") as arq:
        previsto = struct.unpack_from("<IHH", arq.read(32), 4)
    with dbf.open("rb") as arq:
        n, inicio, largura = struct.unpack_from("<IHH", arq.read(32), 4)
        assert previsto == (n, inicio, largura)
        arq.seek(inicio)
        # Distingue registros que coincidem apenas na projeção de campos analíticos.
        assinaturas = []
        for _ in range(n):
            linha = arq.read(largura)
            assert len(linha) == largura and linha[:1] == b" ", "Registro truncado ou excluído"
            assinaturas.append(hashlib.sha256(linha).digest())
    dados = pd.DataFrame(registros(dbf, REQUIRED[tipo]))
    dados["assinatura_registro"] = assinaturas
    return dados


def executar():
    coleta = raiz / "coleta_df"
    manifesto = pd.read_csv(coleta / "manifesto.csv", sep=";", dtype=str)
    esperado = {(m, t, f"{t}DF{m[2:]}.dbc") for m in MESES for t in PASTAS}
    assert len(manifesto) == 39 and set(zip(manifesto.competencia, manifesto.base, manifesto.arquivo)) == esperado
    assert set(coleta.rglob("*.dbc")) == {coleta / m / nome for m, _, nome in esperado}
    hashes, mensal, chaves, painel = [], [], [], []
    for r in manifesto.itertuples():
        p = coleta / r.competencia / r.arquivo
        ficha = json.loads(Path(str(p) + ".json").read_text(encoding="utf8"))
        h = hash_arquivo(p)
        ok = h == r.sha256 == ficha["sha256"] and p.stat().st_size == int(r.bytes) and r.status == "obtido"
        hashes.append(dict(competencia=r.competencia, arquivo=r.arquivo, esperado=r.sha256, antes=h, ok=ok))
    salvar(hashes, "hashes.csv")
    assert all(r["ok"] for r in hashes)
    for m in MESES:
        with TemporaryDirectory() as temp:
            rd, st, lt = [prepare(ler_dbc(coleta / m / f"{t}DF{m[2:]}.dbc", t, Path(temp)), t, m) for t in PASTAS]
        view = integrate(rd, st, lt)
        audit = conferir_chaves(rd, view)
        ref = pilot(rd, st, lt)
        if m == "202506":
            anterior = json.loads((raiz / "evidencias/junho/conservacao_por_chave.json").read_text(encoding="utf8"))
            assert sorted(audit, key=lambda x:x["cnes"]) == sorted(anterior, key=lambda x:x["cnes"])
        invalidos = view.leitos_sus.isna() | view.leitos_sus.eq(0)
        assert view.aih_por_leito_sus.isna().equals(invalidos)
        mensal.append(dict(competencia=m, estabelecimentos=len(view), st_linhas=len(st), lt_linhas=len(lt),
                           **ref, diferenca_registros=ref["aih_depois"]-len(rd),
                           diferenca_centavos=ref["valor_integracao_centavos"]-ref["valor_original_centavos"],
                           chaves_divergentes=0, razoes_incalculaveis=int(invalidos.sum()),
                           tabnet="pendente"))
        painel.append(view)
        chaves.extend(audit)
        print(m, len(rd), len(view), flush=True)
    for r in hashes:
        r["depois"] = hash_arquivo(coleta / r["competencia"] / r["arquivo"])
        assert r["depois"] == r["antes"]
    salvar(hashes, "hashes.csv")
    salvar(mensal, "mensal.csv")
    salvar(chaves, "conservacao.csv")
    salvar(pd.concat(painel), "painel.csv")


if __name__ == "__main__":
    executar()
