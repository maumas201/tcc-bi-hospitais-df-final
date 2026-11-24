from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from graficos import evolucao
from indicador import exibir_razao

PASTA = Path(__file__).parent / "dados"


def ler(nome, separador=","):
    return ler_csv(PASTA / nome, separador)


@st.cache_data
def ler_csv(caminho, separador):
    return pd.read_csv(caminho, sep=separador, dtype={"CNES": str, "cnes": str,
                                                           "competencia": str, "ESPEC": str})


def moeda(centavos):
    reais, resto = divmod(abs(int(centavos)), 100)
    sinal = "-" if centavos < 0 else ""
    return f"{sinal}R$ {reais:,},{resto:02d}".replace(",", ".", f"{reais:,}".count(","))


def mes(valor):
    return valor[4:] + "/" + valor[:4]


st.set_page_config(page_title="Produção hospitalar do DF", layout="wide")
st.title("Produção hospitalar do SUS no Distrito Federal")
dados = ler("painel.csv")
nomes = ler("nomes_consultados.csv").set_index("CNES")["nome_exibicao"].to_dict()
meses = sorted(dados.competencia.unique())
inicio, fim = st.sidebar.select_slider("Período de processamento", meses,
                                       value=(meses[0], meses[-1]), format_func=mes)
unidade = st.sidebar.selectbox("Estabelecimento", ["Todos", *sorted(dados.CNES.unique())],
                               format_func=lambda c: c if c == "Todos" else
                               f"{c} · {nomes.get(c, 'Nome indisponível')}")
recorte = dados[dados.competencia.between(inicio, fim)]
if unidade != "Todos":
    recorte = recorte[recorte.CNES == unidade]

geral, unidades, qualidade = st.tabs(["Visão geral", "Estabelecimentos", "Qualidade e rastreabilidade"])
with geral:
    if recorte.empty:
        st.info("Sem registros de produção para os filtros selecionados.")
    else:
        mensal = recorte.groupby("competencia")[["aih_registros", "valor_total_centavos"]].sum()
        a, b = st.columns(2)
        a.metric("Registros de AIH", f"{recorte.aih_registros.sum():,}".replace(",", "."))
        b.metric("Valor aprovado", moeda(recorte.valor_total_centavos.sum()))
        if inicio != fim:
            mensal = mensal.reindex([m for m in meses if inicio <= m <= fim])
            for coluna, campo, titulo, cor, financeiro in [
                (a, "aih_registros", "Registros de AIH", "#2364A1", False),
                (b, "valor_total_centavos", "R$ milhões", "#00796B", True),
            ]:
                with coluna:
                    st.altair_chart(evolucao(mensal[campo], titulo, cor, financeiro), use_container_width=True)
            st.caption("Cada ponto representa um mês de processamento. Os eixos verticais têm escalas próprias, ajustadas ao recorte.")
        else:
            st.caption(f"Totais da competência {mes(inicio)}.")

with unidades:
    if not recorte.empty and unidade == "Todos":
        st.subheader("Estabelecimentos com maior produção no período")
        ranking = recorte.groupby("CNES").aih_registros.sum().nlargest(10).reset_index()
        ranking["Unidade"] = ranking.CNES.map(nomes).fillna("Nome indisponível") + " · " + ranking.CNES
        grafico = alt.Chart(ranking).mark_bar().encode(
            x=alt.X("aih_registros:Q", title="Registros de AIH"),
            y=alt.Y("Unidade:N", sort="-x", title=None, axis=alt.Axis(labelLimit=340)),
            tooltip=["Unidade", alt.Tooltip("aih_registros:Q", title="AIH")])
        st.altair_chart(grafico, use_container_width=True)
    elif not recorte.empty:
        st.subheader("Leitos SUS cadastrados na unidade por mês")
        serie = recorte.set_index(pd.to_datetime(recorte.competencia, format="%Y%m"))
        st.bar_chart(serie.leitos_sus, y_label="Leitos SUS")
    st.caption("Cada linha representa uma unidade com produção no mês. Os nomes são auxiliares de consulta.")
    tabela = recorte[["CNES", "competencia", "aih_registros", "leitos_existentes", "leitos_sus",
                      "permanencia_media", "n_permanencia_valida"]].copy()
    tabela.insert(1, "Estabelecimento", tabela.CNES.map(nomes).fillna("Nome indisponível"))
    tabela.columns = ["CNES", "Estabelecimento", "Competência", "Registros de AIH",
                      "Leitos existentes", "Leitos SUS", "Permanência média (dias)", "AIH com permanência válida"]
    coluna_razao = "Registros de AIH por leito SUS"
    tabela.insert(6, coluna_razao, [exibir_razao(n, l) for n, l in
                                    zip(recorte.aih_registros, recorte.leitos_sus)])
    st.subheader("Produção e leitos por estabelecimento e mês")
    st.caption("A razão divide os registros de AIH do mês pelos leitos SUS cadastrados na mesma unidade e competência.")
    if len(recorte) == 1:
        linha = recorte.iloc[0]
        a, b, c = st.columns(3)
        a.metric("Registros de AIH no mês", f"{linha.aih_registros:,}".replace(",", "."))
        b.metric("Leitos SUS no mês", "Ausente" if pd.isna(linha.leitos_sus) else str(int(linha.leitos_sus)))
        c.metric(coluna_razao, tabela[coluna_razao].iloc[0])
    st.dataframe(tabela, hide_index=True)
    st.download_button("Baixar tabela filtrada", tabela.to_csv(index=False, sep=";").encode("utf-8-sig"),
                       "estabelecimentos.csv", "text/csv")
    st.subheader("Produção por especialidade da AIH")
    st.caption("Contagem segundo o campo ESPEC do SIH/RD, por código registrado.")
    esp = ler("especialidades.csv").merge(recorte[["CNES", "competencia"]], on=["CNES", "competencia"])
    distribuicao = esp.groupby("ESPEC", as_index=False).registros.sum()
    dominio = ler("dominio_espec.csv").set_index("ESPEC")["Especialidade"]
    distribuicao.insert(1, "Especialidade", distribuicao.ESPEC.map(dominio).fillna("Descrição indisponível"))
    st.dataframe(distribuicao, hide_index=True, column_config={"registros": "Registros de AIH"})

with qualidade:
    st.subheader("Conservação dos registros e do valor aprovado")
    chaves = ["CNES", "competencia"]
    controle = ler("conservacao.csv").rename(columns={"cnes": "CNES"})
    controle = controle[controle.competencia.between(inicio, fim)]
    if unidade != "Todos":
        controle = controle[controle.CNES == unidade]
    pares = controle.merge(recorte, on=chaves, how="outer", validate="one_to_one")
    erros = (pares.registros_antes != pares.aih_registros) | (pares.centavos_antes != pares.valor_total_centavos)
    if pares.empty:
        st.info("Sem pares estabelecimento–competência no recorte.")
    else:
        st.write(f"{len(pares)} pares estabelecimento–competência conferidos · {erros.sum()} com diferença.")
    st.subheader("Comparação mensal do Distrito Federal")
    st.caption("A tabela e o gráfico abaixo abrangem todos os estabelecimentos do DF no período selecionado.")
    ref = ler("comparacao_tabnet.csv", ";")
    fonte = ler("conservacao.csv").groupby("competencia").sum(numeric_only=True)
    integrado = dados.groupby("competencia").sum(numeric_only=True)
    arquivos = ler("hashes.csv")
    arquivos = arquivos[arquivos.competencia.between(inicio, fim)].copy()
    rd = arquivos[arquivos.arquivo.str.startswith("RD")].set_index("competencia").arquivo
    indicador = st.radio("Medida", ["Registros de AIH", "Valor aprovado"], horizontal=True)
    financeiro = indicador == "Valor aprovado"
    medida = "valor_centavos" if financeiro else "aih_aprovadas"
    tabela_df = ref.loc[(ref.medida == medida) & ref.competencia.between(inicio, fim)].set_index("competencia")
    comparacao = pd.DataFrame({
        "Arquivo SIH/RD": rd, "RD antes da integração": fonte.centavos_antes if financeiro else fonte.registros_antes,
        "Painel": integrado.valor_total_centavos if financeiro else integrado.aih_registros,
        "TABNET": tabela_df.tabnet}, index=tabela_df.index)
    comparacao["Painel − RD"] = comparacao["Painel"] - comparacao["RD antes da integração"]
    comparacao["Painel − TABNET"] = comparacao["Painel"] - comparacao["TABNET"]
    comparacao.index = comparacao.index.map(mes)
    comparacao.index.name = "Competência"
    grafico = comparacao[["Painel − TABNET"]].copy()
    if financeiro:
        grafico = grafico / 100
        for campo in comparacao.columns[1:]:
            comparacao[campo] = comparacao[campo].map(moeda)
    st.dataframe(comparacao.reset_index(), hide_index=True, use_container_width=True)
    st.write("Diferença mensal entre o painel e o TABNET")
    st.altair_chart(alt.Chart(grafico.reset_index()).mark_bar().encode(
        x=alt.X("Competência:N", sort=list(grafico.index), title=None),
        y=alt.Y("Painel − TABNET:Q", title="Diferença (R$)" if financeiro else "Diferença (registros)"),
        tooltip=["Competência", "Painel − TABNET"]), use_container_width=True)
    with st.expander("Integridade dos arquivos de origem"):
        st.caption("Comparação dos resumos SHA-256 registrados antes e depois do processamento com o manifesto da coleta.")
        arquivos["Conferência"] = (arquivos.antes.eq(arquivos.esperado) & arquivos.depois.eq(arquivos.esperado)).map(
            {True: "Coincide", False: "Difere"})
        st.dataframe(arquivos.rename(columns={"arquivo":"Arquivo", "competencia":"Competência", "esperado":"SHA-256 do manifesto", "antes":"Antes", "depois":"Depois"}).drop(columns="ok"), hide_index=True)
