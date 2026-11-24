from pathlib import Path

from streamlit.testing.v1 import AppTest

raiz = Path(__file__).resolve().parent
app = AppTest.from_file(str(raiz / "app.py"), default_timeout=30).run()
assert not app.exception
assert len(app.dataframe[1].value) == 10
assert "Descrição indisponível" not in app.dataframe[1].value.Especialidade.tolist()
app.selectbox[0].select("2645157").run()
app.select_slider[0].set_value(("202510", "202510")).run()
assert not app.exception
tabela = app.dataframe[1].value.set_index("ESPEC")
esperado = {"01": ("Cirurgia", 282), "02": ("Obstetrícia", 200),
            "03": ("Clínica médica", 458), "07": ("Pediatria", 185),
            "87": ("Saúde mental", 13)}
assert {c: (r.Especialidade, r.registros) for c, r in tabela.iterrows()} == esperado
assert tabela.registros.sum() == 1138
print("Aprovado: 10 códigos com descrição na série; 5 nomes, contagens e soma em outubro de 2025.")
