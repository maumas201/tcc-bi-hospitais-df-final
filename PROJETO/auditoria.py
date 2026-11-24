"""Conciliação interna por chave com somas independentes das funções analíticas."""
from collections import Counter
from decimal import Decimal
import pandas as pd

def conferir_chaves(rd, visao):
    n, v, incompletas = Counter(), Counter(), set()
    for r in rd.itertuples():
        k = (r.CNES, r.competencia)
        n[k] += 1
        if pd.isna(r.VAL_TOT) or str(r.VAL_TOT).strip() == "":
            incompletas.add(k)
        else:
            v[k] += int(Decimal(str(r.VAL_TOT)) * 100)
    observadas = set()
    registros = []
    for r in visao.itertuples():
        k = (r.CNES, r.competencia)
        if k in observadas or k not in n:
            raise ValueError(f"Chave inesperada ou repetida: {k}")
        observadas.add(k)
        centavos = None if pd.isna(r.valor_total_centavos) else int(r.valor_total_centavos)
        previsto = None if k in incompletas else v[k]
        if int(r.aih_registros) != n[k] or centavos != previsto:
            raise ValueError(f"Divergência na chave {k}")
        registros.append(dict(cnes=k[0], competencia=k[1], registros_antes=n[k],
                              registros_depois=int(r.aih_registros), centavos_antes=previsto,
                              centavos_depois=centavos))
    if observadas != set(n):
        raise ValueError("Produção perdida na integração")
    return registros
