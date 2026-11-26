# Reexecução da versão avaliada do TCC

Repositório: https://github.com/maumas201/tcc-bi-hospitais-df-final/tree/09f2817ca8a9d60fe1cfa21656f9b7f8a931a76b

Execução técnica complementar feita em Linux, em um clone da revisão acima, usando o ZIP da coleta preservada enviado pelos autores. Os scripts executados são os do commit. Antes do processamento, os SHA-256 dos 39 DBC foram confrontados com processamento/manifesto_publico.csv. Foram extraídos do ZIP somente coleta_df/manifesto.csv, os DBC e suas fichas JSON. Os registros individuais de AIH ficam fora deste pacote.

## Como ler as evidências

- ambiente.json identifica o ZIP por SHA-256, a revisão do Git e as versões de Python e das bibliotecas principais. Foi usado um ambiente virtual com acesso aos pacotes do sistema e as versões fixadas nos dois arquivos de dependências do projeto.
- 01_integracao.txt registra o comando, a saída mensal e o código de saída do processamento dos originais.
- 02_especialidades.txt registra o recálculo da produção por especialidade.
- 03_comparacao.txt registra o confronto dos cinco CSV reconstruídos com os CSV da revisão avaliada. A comparação considera cabeçalhos, ordem e conteúdo dos campos. Os hashes identificam os bytes dos DBC de entrada.
- 04_regressao_detalhada.txt mostra os sete casos de regressão individualmente. Os dados controlados de alguns casos provocam falhas deliberadas para exercitar os controles.
- 05_aplicacao_e_tabnet.txt registra o verificador da aplicação, os testes de filtros, P2, especialidades, a regressão e a conciliação mensal com as exportações preservadas. Os testes de interface usam AppTest. Avisos da biblioteca aparecem junto à saída dos scripts.
- resultado.json resume a conservação interna. conservacao.csv, hashes.csv e mensal.csv são saídas desta execução. O campo histórico “tabnet” em mensal.csv pertence à etapa de integração. O resultado da conciliação é produzido e conferido separadamente em verificar.py.

Os horários dos logs identificam esta execução em UTC. A [verificação no Windows](../verificacao_windows.txt) é complementar. Consulte também [a configuração de hardware informada](hardware_informado_windows.png) e [as datas de modificação das exportações TABNET](tabnet_datas_modificacao_exportacoes.png).

## Como reproduzir em outro clone

No terminal, confira o commit com `git rev-parse HEAD`. Na pasta `versao_avaliada`, instale os dois arquivos de dependências com o mesmo Python 3.12. Em uma cópia de trabalho nova, extraia do ZIP a pasta `coleta_df` dentro de `versao_avaliada/processamento`. Confira se o manifesto está em `processamento/coleta_df/manifesto.csv`.

Com esse Python, a partir de `processamento`:

```text
python analisar.py .
python especialidades.py coleta_df --saida especialidades.csv
python conferir_reconstrucao.py
python -m unittest discover -s tests -v
```

Na pasta pai `versao_avaliada`, use `python verificar.py`. No PowerShell, se o ambiente não estiver ativado, substitua `python` pelo caminho do interpretador: `..\.venv\Scripts\python.exe` em processamento e `.\.venv\Scripts\python.exe` em versao_avaliada. O verificador da aplicação pode ser executado isoladamente com os agregados publicados e o requirements.txt da aplicação.

## Informações fornecidas pelo autor

Windows 11 Home 25H2, sistema de 64 bits e processador x64. AMD Ryzen 5 5600 (seis núcleos, 3,50 GHz), 16 GB de RAM e NVIDIA GeForce RTX 3060 com 12 GB. A captura documenta a configuração da máquina informada. O log complementar Linux documenta outra execução.

Na captura do Explorador do Windows, a coluna exibida é “Data de modificação”. Exportação mensal sih_cnv_nidf165441138_0_247_22.csv: 23/11/2026 às 16h54. Exportação por estabelecimento sih_cnv_nidf201212138_0_247_22.csv: 23/11/2026 às 20h12. Os nomes coincidem com as exportações versionadas. Para identificar esses horários como download, é necessária evidência de download ou declaração dos autores sobre como os arquivos foram salvos.
