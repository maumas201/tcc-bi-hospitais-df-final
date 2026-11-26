# Evidências complementares de avaliação técnica — 26/11/2026

Protótipo de integração SIH/RD e CNES/ST/LT no DF. Revisão do código avaliado: [09f2817ca8a9d60fe1cfa21656f9b7f8a931a76b](https://github.com/maumas201/tcc-bi-hospitais-df-final/tree/09f2817ca8a9d60fe1cfa21656f9b7f8a931a76b).
O registro de metadados TABNET foi efetuado sobre a revisão documental `60a541c2da0736c12d0d7a99bfe9bd1c2c644f33`. As evidências complementares estão organizadas separadamente do código avaliado.

## Índice

| Evidência | Caminho | Resultado e alcance |
|---|---|---|
| Matriz de testes | [matriz_testes.csv](matriz_testes.csv) | Identificadores, entrada, esperado, observado e situação |
| Auditoria dos RD e LT | [windows/](windows/) | 13 RD + 13 LT com hashes confrontados; 265.907 registros, 7.305 linhas LT |
| Repetições | [analise_repeticoes_aih.csv](windows/analise_repeticoes_aih.csv) | 143 excedentes por identificador dentro do mês; sem atribuir causa administrativa |
| Indicadores | [validacao_indicadores.csv](windows/validacao_indicadores.csv) | 6.832 comparações, zero divergências, tolerância absoluta 1e-8 |
| Comparação entre ambientes | [comparacao_ambientes_verificada.csv](windows/comparacao_ambientes_verificada.csv) | Quatro relatórios com SHA-256 iguais |
| Reconstrução integral Windows | [Procedimento e logs](windows/reconstrucao_integral.md) | 39 DBC, cinco tabelas aprovadas; três códigos de saída 0 |
| Execução Linux | [referencia/](referencia/) | Registro da reexecução complementar em Linux, com auxílio de IA |
| Ambiente e execução Windows | [windows/](windows/) | Metadados, pacotes antes e depois da instalação do conversor, revisão do código e log original com código de saída 0 |
| TABNET | [tabnet.csv](windows/tabnet.csv) | Datas locais e identidade SHA-256 das duas exportações; não prova horário exato da consulta |
| Exportação | [estabelecimentos.csv](interface/estabelecimentos.csv) | Três competências do Hospital da Região Leste, valores conferidos com referência DBF |
| Acessibilidade | [avaliação](interface/avaliacao_acessibilidade.md) | Seis tarefas concluídas após nova tentativa, uma amostra de contraste insuficiente |
| Desempenho | [desempenho/](desempenho/) | Três rodadas válidas, nove medições AppTest; não mede navegador ou rede |

## Método e limites

Os relatórios Linux e Windows usam o mesmo script `auditar.py`, o mesmo leitor DBF do projeto e conversores diferentes (C no Linux; pyreaddbc no Windows). O recálculo é independente das funções de agregação, mas não das fontes nem de toda a cadeia de leitura. O script complementar verifica os 26 DBC RD e LT; a reconstrução integral das cinco tabelas, conferida em Windows e Linux, utiliza os 39 DBC. A cobertura dos 427 pares refere-se às unidades com produção. Unicidade de chaves LT não comprova unicidade física de camas. Os 143 excedentes são soma de diferenças mensais, não contagem de pacientes ou identificadores distintos de toda a série.

O registro TABNET apresenta os arquivos mensais (jun/2025–jul/2026, recorte analítico até jun/2026) e por estabelecimento (mai/2026). Os hashes coincidem com as cópias publicadas; os filtros adicionais não recuperados pelo cabeçalho não são presumidos. A divergência externa permanece sem causa determinada.

### Desempenho

Protocolo de 26/11/2026: primeira chamada `AppTest.run()` em cada um de três processos Python, seguida de filtros sequenciais de competência e estabelecimento no mesmo AppTest. Medição por `perf_counter`. A importação de AppTest, a criação do processo, a renderização no navegador e a rede não fazem parte do intervalo cronometrado; cache de disco do sistema operacional não controlado. Não houve meta temporal previamente definida nem teste de carga.

| Operação | Mediana (s) | Mínimo (s) | Máximo (s) |
|---|---:|---:|---:|
| Primeira execução AppTest | 1,238694 | 1,216017 | 1,365614 |
| Filtro competência | 0,044105 | 0,043038 | 0,044193 |
| Filtro estabelecimento | 0,045183 | 0,045051 | 0,045243 |

Três processos terminaram com código 0. Os cartões exibiram os valores esperados nas nove medições. A primeira tentativa anterior a esta série falhou por caminho de importação de `graficos.py` no script externo. A execução válida configurou `PYTHONPATH` apontando para a pasta da aplicação, sem alterar o código avaliado. A tentativa malsucedida foi preservada no acervo local e excluída das medições válidas.

### Reprodução complementar no Windows

Use clone limpo da revisão avaliada, Python 3.12 e instale os dois arquivos de dependências da aplicação e do processamento. Para auditoria, indique a pasta `coleta_df` histórica preservada. Não inclua microdados em commits públicos. Execute `auditar.py` com argumentos `CAMINHO_VERSAO_AVALIADA CAMINHO_COLETA_DF PASTA_SAIDA_NOVA`. Para repetir o ensaio AppTest, configure `$env:PYTHONPATH` com o caminho absoluto de `versao_avaliada`, entre nessa pasta e execute `medir_desempenho_tcc.py CAMINHO_VERSAO_AVALIADA PASTA_SAIDA_NOVA` com o mesmo interpretador. O script exige revisão avaliada sem alterações versionadas.

Para reproduzir o registro de TABNET, utilize o clone da revisão documental que contém as duas exportações, os CSV locais preservados e `registrar.ps1` (argumentos `-Versao` e `-OriginaisTabnet`). Não atribua a uma nova coleta os metadados históricos.

## Alcance da avaliação

Os ensaios não demonstram equivalência integral com o TABNET, conformidade completa de acessibilidade, utilidade percebida por profissionais ou escalabilidade. A aquisição histórica e a reconstrução integral em Windows e Linux são distinguíveis da auditoria complementar de 26 arquivos RD/LT. A [cronologia de execução em Windows](windows/registro_execucao.md) apresenta os registros por etapa. A [documentação da proveniência](../fontes/README.md) identifica as fontes e os procedimentos de preservação.
