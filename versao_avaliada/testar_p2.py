from pathlib import Path
from tempfile import TemporaryDirectory
from shutil import copy2, copytree
import pandas as pd
from streamlit.testing.v1 import AppTest

raiz = Path(__file__).resolve().parent
campo = "Registros de AIH por leito SUS"


def consultar(pasta):
    app = AppTest.from_file(str(pasta / "app.py"), default_timeout=30).run()
    app.select_slider[0].set_value(("202510", "202510")).run()
    app.selectbox[0].select("2645157").run()
    assert not app.exception
    return app


def conferir(app, esperado):
    tabela = app.dataframe[0].value
    assert len(tabela) == 1 and tabela.iloc[0][campo] == esperado
    assert next(m.value for m in app.metric if m.label == campo) == esperado


app = consultar(raiz)
conferir(app, "4,63")
linha = app.dataframe[0].value.iloc[0]
assert linha["Registros de AIH"] == 1138 and linha["Leitos SUS"] == 246
app.select_slider[0].set_value(("202510", "202512")).run()
assert list(app.dataframe[0].value[campo]) == ["4,63", "4,45", "5,54"]
print("APROVADO | Hospital da Região Leste | out-dez/2025 | 4,63; 4,45; 5,54")

for leitos, esperado in [(0, "Não calculável (zero leitos SUS)"),
                         (None, "Não calculável (quantidade de leitos SUS ausente)")]:
    with TemporaryDirectory() as tmp:
        pasta = Path(tmp) / "app"
        pasta.mkdir()
        for modulo in ("app.py", "indicador.py", "graficos.py"):
            copy2(raiz / modulo, pasta / modulo)
        copytree(raiz / "dados", pasta / "dados")
        csv = pasta / "dados/painel.csv"
        dados = pd.read_csv(csv, dtype={"CNES": str})
        caso = (dados.CNES == "2645157") & (dados.competencia == 202510)
        dados.loc[caso, "leitos_sus"] = leitos
        dados.to_csv(csv, index=False)
        app = consultar(pasta)
        conferir(app, esperado)
        print("APROVADO | Cenário sintético |", esperado)
