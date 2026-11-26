# Reconstrução integral em ambiente Windows

Execução de 26/11/2026, sobre a revisão avaliada `09f2817ca8a9d60fe1cfa21656f9b7f8a931a76b`, em cópia isolada do código e da coleta histórica.

O processamento utilizou `analisar.py .`, `especialidades.py coleta_df --saida especialidades.csv` e `conferir_reconstrucao.py`, com o interpretador Python 3.12 do ambiente Windows já documentado. O programa de conferência verifica os SHA-256 dos 39 DBC contra o manifesto público e compara cabeçalhos, ordem e valores dos cinco CSV. A comparação não exige identidade binária dos CSV entre plataformas.

Os três logs originais foram preservados em UTF-16LE, conforme registrados pelo PowerShell. A transcrição a seguir facilita sua consulta no GitHub; os arquivos originais permanecem disponíveis. O horário preciso da execução não consta dos logs.

## [01_integracao_windows.log](01_integracao_windows.log)

```text
202506 21120 32
202507 21591 29
202508 20541 33
202509 20874 33
202510 20829 31
202511 19793 31
202512 20360 32
202601 19534 32
202602 18350 35
202603 20438 34
202604 19768 34
202605 21522 35
202606 21187 36
codigo_saida=0
```

## [02_especialidades_windows.log](02_especialidades_windows.log)

```text
427 chaves, 265907 registros, 1222 grupos
codigo_saida=0
```

## [03_reconstrucao_windows.log](03_reconstrucao_windows.log)

```text
APROVADO | painel.csv
APROVADO | conservacao.csv
APROVADO | hashes.csv
APROVADO | especialidades.csv
APROVADO | mensal.csv
codigo_saida=0
```

## Síntese

As 13 competências totalizaram 265.907 registros e 427 pares estabelecimento–competência. A distribuição por especialidade apresentou 1.222 grupos. As cinco tabelas foram aprovadas e os três processos terminaram com código de saída 0. A reconstrução em Windows complementa a auditoria RD/LT e a reexecução em Linux. Os resultados não demonstram equivalência com o TABNET nem avaliação por pesquisadores independentes.
