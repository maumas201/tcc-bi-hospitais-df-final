"""Compara uma transcrição normalizada dos CSV oficiais, conservados separadamente."""
import csv
import sys
from decimal import Decimal
from pathlib import Path

raiz = Path(__file__).resolve().parent
def ler(p):
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))
externos = ler(Path(sys.argv[1]))
with (raiz / "dados/mensal.csv").open(encoding="utf-8-sig") as f:
    local = {r["competencia"]:r for r in csv.DictReader(f)}
if len(externos) != len(local) or {r["competencia"] for r in externos} != set(local):
    raise ValueError("Exigida uma linha para cada uma das 13 competências.")
linhas = []
for r in sorted(externos,key=lambda r:r["competencia"]):
    m = r["competencia"]
    valor = Decimal(r["valor_reais"].replace(",", ".")) * 100
    if valor != valor.to_integral_value() or not valor.is_finite():
        raise ValueError("Valor financeiro inválido")
    for medida,ref,obs in [
        ("aih_aprovadas",int(r["aih_aprovadas"]),int(local[m]["rd_linhas"])),
        ("valor_centavos",int(valor),int(local[m]["valor_original_centavos"]))]:
        dif = obs-ref
        linhas.append([m,medida,obs,ref,dif,abs(dif),str(100*Decimal(abs(dif))/abs(ref)) if ref else "", "coincide" if dif==0 else "investigar"])
destino=raiz / "comparacao_tabnet.csv"
with destino.open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.writer(f,delimiter=";")
    w.writerow(["competencia","medida","local","tabnet","diferenca","absoluta","relativa_pct","resultado"])
    w.writerows(linhas)
print(destino)
