"""Confronta as saídas de analisar.py e especialidades.py com a versão avaliada."""
from pathlib import Path
import csv
import hashlib

pasta = Path(__file__).resolve().parent
with (pasta / "manifesto_publico.csv").open(encoding="utf-8-sig") as stream:
    for registro in csv.DictReader(stream):
        origem = pasta / "coleta_df" / registro["competencia"] / registro["arquivo"]
        with origem.open("rb") as dados:
            if hashlib.file_digest(dados, "sha256").hexdigest() != registro["sha256"]:
                raise ValueError(f"Versão de origem divergente: {origem.name}")


def ler(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.reader(stream))


for nome in ("painel", "conservacao", "hashes", "especialidades", "mensal"):
    referencia = pasta.parent / ("conciliacao/dados" if nome == "mensal" else "dados")
    arquivo = nome + ".csv"
    if ler(pasta / arquivo) != ler(referencia / arquivo):
        raise ValueError(f"Reconstrução divergente: {arquivo}")
    print(f"APROVADO | {arquivo}")
