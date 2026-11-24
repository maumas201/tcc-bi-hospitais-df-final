from pathlib import Path
import pandas as pd
from streamlit.testing.v1 import AppTest

raiz = Path(__file__).parent
controle = pd.read_csv(raiz / "dados/conservacao.csv", dtype={"cnes": str, "competencia": str})
app = AppTest.from_file(str(raiz / "app.py"), default_timeout=30).run()
assert not app.exception
assert [m.value for m in app.metric] == ["265.907", "R$ 469.282.753,25"]
assert len(app.dataframe[0].value) == 427
for mes in sorted(controle.competencia.unique()):
    app.select_slider[0].set_value((mes, mes)).run()
    assert not app.exception
    mensal = controle[controle.competencia == mes]
    assert int(app.metric[0].value.replace(".", "")) == mensal.registros_antes.sum()
    moeda = app.metric[1].value.removeprefix("R$ ").replace(".", "").replace(",", "")
    assert int(moeda) == mensal.centavos_antes.sum()
    assert app.dataframe[1].value.registros.sum() == mensal.registros_antes.sum()

mes = "202506"
app.select_slider[0].set_value((mes, mes)).run()
app.selectbox[0].select("0010456").run()
assert not app.exception
assert app.metric[0].value == "2.511"
assert app.metric[1].value == "R$ 7.590.382,95"
assert len(app.dataframe[0].value) == 1
assert app.dataframe[2].value.iloc[0]["TABNET"] == 21120
ausentes = set(controle.cnes) - set(controle.loc[controle.competencia == mes, "cnes"])
app.selectbox[0].select(sorted(ausentes)[0]).run()
assert not app.exception and app.info and app.dataframe[0].value.empty
print("Aprovado: série completa, 13 competências, filtro combinado, referência distrital e recorte vazio.")
app.selectbox[0].select("Todos").run()
app.select_slider[0].set_value(("202506", "202606")).run()
comp = app.dataframe[2].value
assert comp["Painel − RD"].eq(0).all() and comp["Painel − TABNET"].sum() == 20
assert len(comp) == 13 and comp["Arquivo SIH/RD"].nunique() == 13
app.radio[0].set_value("Valor aprovado").run()
comp = app.dataframe[2].value
assert not app.exception and comp["Painel − RD"].eq("R$ 0,00").all()
assert comp.loc[comp["Competência"] == "05/2026", "Painel − TABNET"].item() == "R$ 3.964,81"
assert len(app.dataframe[3].value) == 39 and app.dataframe[3].value["Conferência"].eq("Coincide").all()
print("Aprovado: comparação de três fontes, gráficos, moeda e manifesto de 39 arquivos.")
