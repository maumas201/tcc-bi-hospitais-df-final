# Registro de execução em ambiente Windows

**Autores:** Maurício Rafael Oliveira da Silva e Gabriel Silva dos Santos.  
**Execução técnica em Windows:** Maurício Rafael Oliveira da Silva.  
**Revisão avaliada:** `09f2817ca8a9d60fe1cfa21656f9b7f8a931a76b`.

## Ambiente

O registro de 26/11/2026 às 15h05min29s (UTC−03) identifica Windows 11 Home 25H2, 64 bits, build 26200.9974, AMD Ryzen 5 5600 (6 núcleos), 15,9 GiB de RAM, NVIDIA GeForce RTX 3060, PowerShell 5.1.26100.9818, Git 2.53.0.windows.1 e Python 3.12.10. A coleta de metadados do TABNET ocorreu sobre o commit documental `60a541c2da0736c12d0d7a99bfe9bd1c2c644f33`. A auditoria ocorreu sobre a revisão avaliada. Os arquivos [ambiente.json](ambiente.json), [pacotes.json](pacotes.json), [pacotes_auditoria.json](pacotes_auditoria.json) e [commit_auditado.txt](commit_auditado.txt) registram essas condições. Os pacotes de auditoria incluem pyreaddbc 2.0.4 e dbfread 2.0.7, instalados após a primeira coleta de metadados.

## Cronologia e evidências

| Etapa | Data e resultado | Registro |
|---|---|---|
| Aquisição histórica de RD/ST/LT | 23/11/2026; 39 arquivos, 13 competências, URLs, horários e SHA-256 | [Manifesto público](../../../versao_avaliada/processamento/manifesto_publico.csv) |
| Exportações TABNET | Criação local em 23/11/2026, às 16h54min52s e 20h12min19s; identidade de conteúdo verificada | [Metadados](tabnet.csv) |
| Verificação da aplicação e regressão | 26/11/2026, 00h57; código de saída 0, sete testes | [Log Windows](../../../versao_avaliada/evidencias/verificacao_windows.txt) |
| Preparação do ambiente e registro TABNET | 26/11/2026, 15h05; dois hashes coincidentes | [Ambiente](ambiente.json), [TABNET](tabnet.csv) |
| Auditoria complementar RD/LT | 26/11/2026, pasta de execução identificada por 15h11min30s; 26 DBC, 6.832 comparações, zero divergências ou exceções | [Log](auditoria-20261126-151130.log), [relatório](validacao_indicadores.csv) |
| Interface e exportação | 26/11/2026; três linhas exportadas, seis tarefas por teclado concluídas após reteste, contraste amostral 3,69:1 | [Inspeção](../interface/avaliacao_acessibilidade.md), [CSV](../interface/estabelecimentos.csv) |
| Desempenho | 26/11/2026; três rodadas válidas, nove medições, três códigos de saída 0 | [Método](../desempenho/metodo.json), [resultados](../desempenho/desempenho.csv) |
| Reconstrução integral | 26/11/2026; 39 DBC, 13 competências, 427 pares, cinco tabelas aprovadas, três códigos de saída 0 | [Procedimento e logs](reconstrucao_integral.md) |

Os registros de aquisição históricos não constituem uma nova aquisição em 26/11/2026. O manifesto registra os horários da coleta de 23/11/2026; as datas de criação dos CSV TABNET identificam as cópias locais, não o instante exato da consulta. A auditoria complementar de Windows recalculou as medidas RD/LT a partir da coleta preservada. A reconstrução das cinco tabelas desde os 39 DBC foi conferida em [Windows](reconstrucao_integral.md) e em [Linux](../../../versao_avaliada/evidencias/evidencias_reexecucao/LEIA-ME.md). A execução Linux foi realizada com auxílio de IA. As verificações não constituem reprodução externa por pesquisadores independentes.

## Procedimento complementar executado

Em um clone da revisão avaliada, foram instaladas as dependências da aplicação e do processamento. O arquivo histórico foi extraído sem nova transferência dos DBC. A auditoria foi executada com o interpretador do ambiente virtual, passando os caminhos da revisão avaliada, de `coleta_df` e da pasta de saída. O comando foi registrado com `Tee-Object` e o código de saída foi acrescentado ao log. Os hashes dos quatro relatórios foram confrontados com os da execução Linux. Os arquivos coincidiram byte a byte. Para o ensaio de desempenho, configurou-se `PYTHONPATH` para a pasta da aplicação; os intervalos foram registrados por `perf_counter` em três processos separados.

O procedimento preserva o código avaliado. Os arquivos de saída originais e os logs foram mantidos sem correção textual; caracteres acentuados do log Windows apresentam uma diferença de codificação.
