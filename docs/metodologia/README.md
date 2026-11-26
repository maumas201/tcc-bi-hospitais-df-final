# Fundamentação documental, requisitos e trabalhos correlatos

## Derivação documental das personas

A análise documental foi utilizada para identificar tarefas de consulta e monitoramento pertinentes ao recorte do artefato. Para cada documento, foram identificados a finalidade do indicador, as dimensões de consulta, os elementos de cálculo e as limitações. Em seguida, os elementos compatíveis com os arquivos disponíveis foram relacionados a comportamentos verificáveis do sistema. Os perfis P1, P2 e P3 constituem representações hipotéticas elaboradas pelos autores, e não resultados de entrevistas ou observações de usuários. A complementação documental de 26 de novembro de 2026 conferiu os procedimentos e fichas da SES-DF e confrontou-os com os cenários previamente implementados.

O indicador 19 do Caderno de Orientações AGL Hospitalar (Distrito Federal, 2025, p. 110–112) fundamenta a consulta por período e estabelecimento. O projeto adapta essas dimensões à competência de processamento e ao CNES, sem reproduzir o percentual oficial de tempestividade de AIH ou o filtro de região de saúde. Os indicadores 7 e 8 do mesmo caderno (p. 77–82) fundamentam a pertinência de relacionar atividade e estrutura hospitalar. Entretanto, a razão proposta utiliza registros RD e estoque cadastral mensal de leitos SUS, não saídas de pacientes ou leitos operacionais diários. Portanto, não substitui os indicadores institucionais de ocupação ou giro de leitos. A literatura sobre exploração de dados hospitalares e avaliação de integração (Pedroso et al., 2025; Shimaoka et al., 2026) fundamenta o perfil analítico voltado à rastreabilidade. O vínculo entre os perfis, os requisitos e os testes é explicitado no Apêndice A. As verificações são técnicas e não demonstram aceitação, utilidade percebida ou adequação ao fluxo de trabalho de profissionais reais.

## Matriz de rastreabilidade

A matriz conserva RF1–RF3 e RN1–RN2, desdobra RN3 em segurança/minimização (RN3a) e desempenho (RN3b) e inclui RF4 (exportação). Os identificadores de teste abaixo correspondem à matriz consolidada. A matriz consolida retrospectivamente as funções e os critérios, salvo aqueles já registrados nos protocolos de teste.

| ID | Origem/perfil | Critério de aceite/avaliação | Testes | Resultado e limites |
|---|---|---|---|---|
| RF1 | P1, AGL indicador 19, p. 110–112 | Filtrar período/CNES; contagem e centavos iguais à referência; estado vazio coerente | UI-01, T1 | Aprovado nos cenários registrados; Região Leste out/25: 1.138 e R$ 866.173,53 |
| RF2 | P2, AGL indicadores 7–8; razão definida pelos autores | Exibir produção, estoque SUS e razão mensal; distinguir denominador zero e ausente | P2-01, REG-7, DADOS, T2 | 4,63; 4,45; 5,54; condições sintéticas conferidas. Não é giro ou ocupação |
| RF3 | P3, literatura; decisão de projeto | Identificar recorte, origem e diferenças internas e externas sem ocultar discrepâncias | UI-02, TAB-01, TAB-02, T3 | Rastreabilidade nos casos examinados; diferença externa permanece |
| RF4 | P1/P2/P3, decisão de projeto | Exportar exatamente as linhas do recorte selecionado | P2-CSV | 3 linhas, CNES 2645157, out–dez/25, valores conferidos |
| RN1 | Integridade e reprodutibilidade | Unicidade por chave; conservação em contagens/centavos; reconstrução e hashes | REG-1–7, INT-01/02, RD-01/02, LT-01, DADOS, REP-01 | Conservação 427 pares; cinco tabelas reconstruídas em Windows e Linux; 6.832 comparações com tolerância 1e-8; 4 relatórios idênticos |
| RN2 | Acessibilidade amostral; WCAG 2.2, 1.4.3 | Tarefas por teclado, foco visível, rótulos e alternativas tabulares; texto comum >=4,5:1 | AC01–08 | 6 tarefas concluídas após reteste; texto 3,69:1 não atende. Sem avaliação integral |
| RN3a | Minimização de dados; decisão de projeto | Distribuir saídas agregadas e não publicar microdados | Inspeção dos CSV distribuídos; PUBLICO | Agregados disponíveis no pacote; acesso anônimo não avaliado; sem auditoria de segurança |
| RN3b | Desempenho; decisão de projeto | Medir três operações em três rodadas e conferir valores | PERF-01–03 | Medianas 1,238694 s, 0,044105 s e 0,045183 s; sem limiar prévio, sem teste de carga |

## Escolhas tecnológicas

| Tecnologia | Alternativas | Justificativa para o recorte | Limite |
|---|---|---|---|
| pandas 2.3.3 | SQL/SQLite, Polars | Agregação e validação de cardinalidade em Python; fluxo e testes no mesmo ambiente | Memória local; sem benchmark comparativo |
| Streamlit 1.50.0 | Dash, frontend + API, Power BI | Interface e filtros em Python, AppTest, código versionável; execução local | Menor liberdade de personalização; contraste amostral insuficiente |
| Altair 5.5.0 | Plotly, Matplotlib | Especificação declarativa de marca, eixo, tipo e unidade; adequada às séries e rankings agregados | Não se demonstrou superioridade; legibilidade requer inspeção |
| CSV | SQLite/PostgreSQL, Parquet | 427 linhas na tabela principal; inspeção e intercâmbio sem servidor; hashes de arquivos | Tipos precisam ser definidos na leitura; sem transações, índices ou acesso concorrente |

As escolhas são proporcionais ao recorte implementado, não uma comparação empírica de desempenho, custo ou manutenção. A escolha de CSV é da camada analítica distribuída, não dos arquivos DBC originais. A validação de junção em pandas não substitui o controle da granularidade nem os testes de conservação.

## Complementação bibliográfica

Data: 26/11/2026. Tipo: conferência de seleção intencional já existente, não revisão sistemática. Consultados por título/autor: anais SBCAS (DOI e cópia disponibilizada pelo autor), repositórios UFCSPA e IFSP, revista Asklepion. Consultas documentais: Caderno AGL Hospitalar 2025, indicador AIH, giro de leitos, ocupação operacional e Infosaúde CNES × Sistemas de Produção. Consultas técnicas: pandas merge validate, Streamlit AppTest, Altair declarative encodings. Recorte das obras aplicadas: 2024–2026, além de documentos institucionais. Critérios de pertinência: exploração de produção, integração/ETL ou visualização de informação em saúde; fonte identificável; descrição de artefato ou avaliação. A complementação não contabilizou todos os resultados dos buscadores nem reconstituiu buscas anteriores sem registros. A seleção não constitui levantamento exaustivo ou revisão sistemática.

## Comparação dos trabalhos correlatos

| Antecedente | Fonte e recorte | Tecnologia | Avaliação | Relação e limite |
|---|---|---|---|---|
| Pedroso et al. (2025) | SIH/SUS, RS | PySUS, Python, Streamlit, Plotly | Demonstração exploratória; resposta elevada em consultas sob demanda | Proximidade temática; recorte deste trabalho pré-agregado e testes de conservação; tempos não comparáveis |
| Ribeiro (2025) | Dados públicos/privados de oncologia pediátrica | ETL e quatro dashboards web; tecnologias específicas não identificadas na consulta | Usabilidade com seis especialistas | Demonstra uma etapa que este estudo não realizou; não comparar resultados clínicos |
| Shimaoka et al. (2026) | SIA-SUS, jan/2024, SC/ES/RN; cerca de 3,2 milhões de registros | ETL em nuvem, PostgreSQL/Supabase | Cinco repetições por cenário; avaliação de tempos | Referência de protocolo; o ensaio AppTest deste trabalho não mede ETL em nuvem ou escalabilidade |
| Brachini (2024) | Registros de dengue de Votuporanga e geocodificação | PostgreSQL, Node.js, Streamlit/Folium | Demonstração de sistema e mapas | Delimitação territorial e interface; outra unidade analítica |
| SES-DF, Infosaúde | Cadastro CNES e regras de consistência SIA/SIH; consulta institucional | Tecnologia interna não identificada na página | Orientação administrativa e exemplo de consistência cadastral | Não é benchmark; não foram inspecionados código, pipeline interno ou equivalência funcional |
| Este TCC | SIH/RD + CNES/ST/LT, DF, 13 competências | Python, pandas, CSV, Streamlit, Altair | Conservação por chave, recálculo, regressão, reprodução, conciliação, interface e desempenho amostral | Divergência TABNET, contraste abaixo do mínimo, ausência de avaliação com usuários |

## Fontes conferidas (acesso em 26 nov. 2026)

- DISTRITO FEDERAL. Secretaria de Estado de Saúde. Caderno de orientações AGL hospitalar 2025. Versão 8. Brasília, DF: SES-DF, 2025. https://info.saude.df.gov.br/wp-content/uploads/2025/06/Caderno-de-Orientacoes-AGL-Hospitalar-2025.pdf — fichas 7, 8 e 19; p. 110 e 112 conferidas visualmente; p. 80 conferida visualmente.
- DISTRITO FEDERAL. Secretaria de Estado de Saúde. Caderno de orientações AGL hospitalar 2025. Versão 9. Brasília, DF: SES-DF, 2025. https://info.saude.df.gov.br/wp-content/uploads/2025/07/Caderno_de_Orientacoes_AGL_Hospitalar_2025_V.9.pdf — confirmação complementar. A versão 8 constitui a referência principal da análise.
- DISTRITO FEDERAL. Secretaria de Estado de Saúde. Painel Infosaúde — CNES x Sistemas de Produção. https://info.saude.df.gov.br/sala-de-situacao/painel-infosaude-cnes-x-sistemas-de-producao/ — documentação institucional, não inspeção da implementação.
- PEDROSO et al. Análise dinâmica de dados hospitalares: uma abordagem interativa para gestão em saúde. 2025. DOI: https://doi.org/10.5753/sbcas_estendido.2025.7234 (resolução direta não acessível nesta consulta); cópia do autor: https://www.researchgate.net/publication/392616306_Analise_Dinamica_de_Dados_Hospitalares_Uma_Abordagem_Interativa_para_Gestao_em_Saude
- RIBEIRO, Felipe de Assis. Visualização de dados aplicada à oncologia pediátrica: auxiliando a descobrir padrões e tendências. 2025. Dissertação — UFCSPA. https://repositorio.ufcspa.edu.br/items/43f9c8df-6c13-4e74-b5e0-5bf954d58bd4/full — metadados e resumo institucional.
- SHIMAOKA et al. Pipeline ETL escalável para ingestão de dados em saúde: aplicação ao Sistema Único de Saúde (SUS). Asklepion, v. 5, n. 1, e132, 2026. https://doi.org/10.21728/asklepion.2026v5n1e-132 ; texto integral: https://revistaasklepion.emnuvens.com.br/asklepion/article/download/132/264?inline=1
- BRACHINI, Maria Tereza Costa. Proposta de uma ferramenta de Business Intelligence para mapeamento de ocorrências de caso de dengue no município de Votuporanga. 2024. TCC — IFSP. https://repositorio.ifsp.edu.br/server/api/core/bitstreams/e9132d9e-d0e6-49ff-bbae-ac012c0581ec/content
- THE PANDAS DEVELOPMENT TEAM. Merge, join, concatenate and compare. Documentação 2.3.3. https://pandas.pydata.org/pandas-docs/version/2.3.3/user_guide/merging.html
- STREAMLIT. App testing. https://docs.streamlit.io/develop/api-reference/app-testing — documentação do recurso, não prova de versão instalada.
- VEGA-ALTAIR. Overview. https://altair-viz.github.io/getting_started/overview.html — conceito declarativo; versão da documentação pode diferir da instalada.
- W3C. WCAG 2.2, SC 1.4.3. https://www.w3.org/TR/WCAG22/#contrast-minimum

