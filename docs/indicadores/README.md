# Fichas técnicas dos indicadores

Revisão avaliada: [09f2817](https://github.com/maumas201/tcc-bi-hospitais-df-final/tree/09f2817ca8a9d60fe1cfa21656f9b7f8a931a76b). Recorte: DF, competências de processamento 202506–202606. Unidade analítica: CNES × competência com produção RD. A definição abaixo descreve a implementação, não substitui fichas oficiais do Ministério da Saúde ou SES-DF.

## Regras comuns

O código valida CNES, competência, município do DF e IDENT 1/5 no RD. Rejeita valores numéricos inválidos, chaves inválidas e duplicações integrais detectadas na entrada; não deduplica N_AIH automaticamente. ST fornece correspondência cadastral; LT é agregado antes da junção. Ausência não é convertida em zero no processamento. Os filtros da interface selecionam competência e estabelecimento; a comparação externa mensal abrange o DF inteiro, independentemente do estabelecimento selecionado.

## I01 — Registros de AIH

- Finalidade: descrever volume de registros administrativos de produção.
- Fonte: SIH/RD; CNES, ANO_CMPT, MES_CMPT, MUNIC_MOV, IDENT, N_AIH.
- Fórmula: número de linhas elegíveis do RD no grupo (IDENT 1 e 5). Soma dos grupos no recorte.
- Unidade: registros. Exemplo: DF, jun/2025 = 21.120; série = 265.907.
- Limite: não representa pacientes únicos, contagem de N_AIH distintos ou necessariamente a medida AIH aprovadas do TABNET. Prorrogações são mantidas.

## I02 — Valor aprovado

- Finalidade: descrever valor administrativo registrado no RD.
- Fonte: SIH/RD, VAL_TOT.
- Fórmula: converter cada valor para centavos inteiros, sem arredondar frações inferiores a centavo; somar por chave. O processamento utiliza soma estrita (ausência em parcela implica total desconhecido). A interface soma os agregados do recorte; o comportamento com valores ausentes não constitui garantia geral de completude.
- Unidade: reais, apresentados com duas casas decimais.
- Exemplo: DF, jun/2025 = R$ 33.972.979,19; série = R$ 469.282.753,25.
- Limite: não equivale necessariamente a desembolso financeiro, custo real, orçamento ou valor conciliado com TABNET.

## I03 — Permanência média

- Finalidade: descrever dias de permanência registrados nas AIHs normais.
- Fonte: SIH/RD, DIAS_PERM e IDENT.
- Fórmula: soma dos dias das linhas IDENT=1 dividida pela quantidade dessas linhas com dias válidos, somente se todas as linhas normais do grupo tiverem dias válidos e houver pelo menos uma. Caso contrário, ausência.
- Unidade: dias; não calcular média simples das médias de unidades ou meses.
- Exemplo: CNES 2645157, out/2025 = 3,9859 dias na tabela exportada.
- Limite: não inclui IDENT=5; competência de processamento não é data de admissão ou alta. Não equivale a medida operacional de permanência de pacientes únicos.

## I04 — Leitos existentes

- Finalidade: consultar estoque cadastral mensal.
- Fonte: CNES/LT, QT_EXIST, TP_LEITO, CODLEITO, CNES, COMPETEN.
- Fórmula: soma estrita de QT_EXIST nas categorias observadas do CNES e competência; ausência em qualquer parcela ou falta de correspondência LT implica indisponibilidade.
- Unidade: leitos cadastrados. Exemplo: CNES 2645157, out/2025 = 246.
- Limite: não soma estoques de meses como capacidade simultânea; não comprova disponibilidade operacional, ocupação ou unicidade física.

## I05 — Leitos SUS

- Finalidade: consultar estoque cadastral vinculado ao SUS.
- Fonte: CNES/LT, QT_SUS; mesmas dimensões de I04.
- Fórmula: soma estrita de QT_SUS por CNES e competência, com controle de QT_SUS <= QT_EXIST quando ambos presentes.
- Unidade: leitos cadastrados SUS. Exemplo: CNES 2645157, out/2025 = 246.
- Limite: não representa leitos-dia, leitos efetivamente disponíveis ou ocupados.

## I06 — Registros de AIH por leito SUS

- Finalidade: relacionar descritivamente produção administrativa e estoque cadastral.
- Fórmula: I01 / I05 na mesma unidade e competência; somente com denominador positivo. Zero e ausência recebem mensagens distintas na interface. Formatação com duas casas decimais.
- Unidade: registros por leito SUS cadastrado no mês.
- Exemplo: CNES 2645157, out/2025: 1.138 / 246 = 4,63; nov/2025: 1.095 / 246 = 4,45; dez/2025: 1.363 / 246 = 5,54.
- Limite: não é percentual, taxa de ocupação, giro de leitos ou produtividade clínica. Não agregar razões por média simples nem interpretar como leitos utilizados.

## I07 — Distribuição por especialidade da AIH

- Fonte: SIH/RD, ESPEC; tabela especialidades.csv e domínio de códigos distribuído.
- Fórmula: contagem de registros por CNES, competência e código ESPEC; soma no recorte. Descrição auxiliar por código.
- Unidade: registros de AIH por especialidade registrada.
- Limite: não equivale a especialidade de leitos do CNES, nem a diagnóstico ou paciente único.

## Medidas auxiliares de qualidade

Conservação: diferença painel menos RD por chave em contagens e centavos. Comparação externa: diferença painel menos TABNET, por competência de processamento e medida, no DF. As duas verificações têm referências distintas. Uma diferença interna nula não implica equivalência externa.

## Código e evidências

- [Transformações e cálculos](../../versao_avaliada/processamento/tccbi/core.py)
- [Interface](../../versao_avaliada/app.py)
- [Formatação da razão](../../versao_avaliada/indicador.py)
- [Tabela analítica](../../versao_avaliada/dados/painel.csv)
- [Conservação](../../versao_avaliada/dados/conservacao.csv)
- [Conciliação externa](../../versao_avaliada/conciliacao/)
