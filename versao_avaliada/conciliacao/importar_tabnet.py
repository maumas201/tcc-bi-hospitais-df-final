"""Normaliza a exportação recebida e confere os subtotais antes do recorte."""
import csv
from pathlib import Path
from decimal import Decimal
import subprocess
import sys

raiz = Path(__file__).resolve().parent
origem, = (raiz / "dados").glob("sih_cnv*.csv")
meses = "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split()
linhas = list(csv.reader(origem.read_text(encoding="latin1").splitlines(), delimiter=";"))
inicio = linhas.index(["Ano/mês processamento","AIH_aprovadas","Valor_total"])
if "por local de internação - Distrito Federal" not in linhas[0][0]:
    raise ValueError("Recorte geográfico divergente")
referencias = {}
controles = {}
for row in linhas[inicio+1:]:
    if len(row) != 3:
        continue
    periodo, n, reais = row
    valor = Decimal(reais.replace(",", "."))
    if "/" in periodo:
        nome, ano = periodo.lower().split("/")
        mes = f"{ano}{meses.index(nome)+1:02}"
        if mes in referencias:
            raise ValueError("Competência repetida")
        referencias[mes] = (int(n),valor)
    else:
        controles[periodo] = (int(n),valor)
for rotulo, esperado in controles.items():
    bloco = [v for m,v in referencias.items() if rotulo=="Total" or m.startswith(rotulo)]
    if tuple(map(sum,zip(*bloco))) != esperado:
        raise ValueError(f"Subtotal divergente: {rotulo}")
destino = raiz / "dados/tabnet_recorte.csv"
with destino.open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f,delimiter=";")
    w.writerow(["competencia","aih_aprovadas","valor_reais"])
    for mes,(n,v) in sorted(referencias.items()):
        if "202506" <= mes <= "202606":
            w.writerow([mes,n,v])
subprocess.run([sys.executable,raiz/"comparar_tabnet.py",destino],check=True)
