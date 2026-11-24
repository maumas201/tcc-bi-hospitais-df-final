import altair as alt
import pandas as pd


def evolucao(serie, titulo, cor, financeiro=False):
    """Desenhar observações mensais em ordem, interrompendo a linha nas lacunas."""
    quadro = pd.DataFrame({"Competência": [m[4:] + "/" + m[:4] for m in serie.index],
                           "Valor": serie.to_numpy()})
    quadro["Trecho"] = quadro.Valor.isna().cumsum()
    escala = 100_000_000 if financeiro else 1
    quadro["Medida"] = quadro.Valor / escala
    def rotulo(n):
        if pd.isna(n):
            return "Sem registro"
        if financeiro:
            reais, cents = divmod(int(n), 100)
            return "R$ " + f"{reais:,}".replace(",", ".") + f",{cents:02d}"
        return f"{int(n):,}".replace(",", ".")
    quadro["Total"] = quadro.Valor.map(rotulo)
    return alt.Chart(quadro).mark_line(point=True, color=cor, strokeWidth=2.6).encode(
        x=alt.X("Competência:O", sort=quadro["Competência"].tolist(), title=None,
                axis=alt.Axis(labelAngle=-40)),
        y=alt.Y("Medida:Q", title=titulo, scale=alt.Scale(zero=False)),
        detail="Trecho:N", tooltip=["Competência:N", "Total:N"]
    ).properties(height=205)
