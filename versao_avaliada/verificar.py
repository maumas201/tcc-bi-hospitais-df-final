"""Execute com o mesmo Python usado para instalar requirements.txt."""
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil

raiz = Path(__file__).resolve().parent


def executar(pasta, *argumentos):
    subprocess.run([sys.executable, *argumentos], cwd=pasta, check=True)


for script in ("conferir_app.py", "testar_p2.py", "conferir_visual.py"):
    executar(raiz, script)
executar(raiz / "processamento", "-m", "unittest", "discover", "-s", "tests")
with tempfile.TemporaryDirectory() as temp:
    copia = Path(temp) / "conciliacao"
    shutil.copytree(raiz / "conciliacao", copia)
    executar(copia, "importar_tabnet.py")
    from csv import reader
    def linhas(path):
        with path.open(encoding="utf-8-sig", newline="") as arq:
            return list(reader(arq, delimiter=";"))
    if linhas(copia / "comparacao_tabnet.csv") != linhas(raiz / "dados/comparacao_tabnet.csv"):
        raise ValueError("Conciliação mensal diferente da versão avaliada.")
print("APROVADO: painel, P2, especialidades, conservação e conciliação mensal.")
