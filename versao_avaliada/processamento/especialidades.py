"""Exporta somente contagens de registros RD, conferidas contra o painel."""
import argparse
import csv
import hashlib
import subprocess
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile, Path as CaminhoZip
from contextlib import ExitStack
from leitor_dbf import registros

pasta = Path(__file__).resolve().parent.parent / "dados"
p = argparse.ArgumentParser()
p.add_argument("origem", type=Path, help="Pasta coleta_df ou ZIP contendo coleta_df/")
p.add_argument("--saida", type=Path, default=pasta / "especialidades.csv")
p.add_argument("--conversor", type=Path)
args = p.parse_args()
with (pasta / "painel.csv").open(encoding="utf-8-sig") as f:
    referencia = {(r["CNES"], r["competencia"]): int(r["aih_registros"]) for r in csv.DictReader(f)}
categorias = Counter()
chaves = Counter()
with ExitStack() as recursos:
    temp = recursos.enter_context(TemporaryDirectory())
    coleta = args.origem
    if coleta.is_file():
        coleta = CaminhoZip(recursos.enter_context(ZipFile(coleta))) / "coleta_df"
    manifesto = csv.DictReader((coleta / "manifesto.csv").read_text(encoding="utf-8-sig").splitlines(), delimiter=";")
    for r in manifesto:
        if r["base"] != "RD":
            continue
        mes = r["competencia"]
        dados = (coleta / mes / r["arquivo"]).read_bytes()
        if hashlib.sha256(dados).hexdigest() != r["sha256"]:
            raise ValueError(f"Hash divergente em {mes}")
        dbc = Path(temp) / "entrada.dbc"
        dbf = Path(temp) / "saida.dbf"
        dbf.unlink(missing_ok=True)
        dbc.write_bytes(dados)
        if args.conversor:
            subprocess.run([str(args.conversor.resolve()), dbc, dbf], check=True)
        else:
            from pyreaddbc import dbc2dbf
            dbc2dbf(str(dbc), str(dbf))
        for row in registros(dbf, ["CNES", "ANO_CMPT", "MES_CMPT", "ESPEC"]):
            if row["ANO_CMPT"] + row["MES_CMPT"] != mes:
                raise ValueError("Competência divergente")
            cnes = row["CNES"]
            chave = (cnes, mes)
            chaves[chave] += 1
            categorias[cnes, mes, row["ESPEC"] or "Ausente"] += 1
if chaves != referencia:
    raise ValueError("Distribuição por especialidade diverge da produção por chave")
with args.saida.open("w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["CNES", "competencia", "ESPEC", "registros"])
    for k, n in sorted(categorias.items()):
        w.writerow([*k, n])
print(len(chaves), "chaves,", sum(chaves.values()), "registros,", len(categorias), "grupos")
