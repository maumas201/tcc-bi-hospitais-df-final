import pandas as pd


def exibir_razao(registros, leitos):
    """Formatar a razão de uma única unidade em uma competência."""
    if pd.isna(leitos):
        return "Não calculável (quantidade de leitos SUS ausente)"
    if leitos == 0:
        return "Não calculável (zero leitos SUS)"
    return f"{registros / leitos:.2f}".replace(".", ",")
