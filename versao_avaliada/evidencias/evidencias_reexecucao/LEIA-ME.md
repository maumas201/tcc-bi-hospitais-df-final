# Avaliação técnica e reprodutibilidade

Repositório: https://github.com/maumas201/tcc-bi-hospitais-df-final/tree/09f2817ca8a9d60fe1cfa21656f9b7f8a931a76b

Os testes iniciais do protótipo foram executados por Maurício Rafael Oliveira da Silva no ambiente Windows descrito neste documento. Para avaliar a reprodutibilidade em outro ambiente, realizamos uma reexecução complementar em Linux com auxílio do ChatGPT, a partir de um clone da revisão acima e do arquivo ZIP da coleta preservada. Os scripts executados correspondem à revisão indicada. Antes do processamento, os SHA-256 dos 39 DBC foram confrontados com processamento/manifesto_publico.csv. Foram extraídos do ZIP somente coleta_df/manifesto.csv, os DBC e suas fichas JSON. Os registros individuais de AIH ficam fora deste pacote.

## Como ler as evidências

- ambiente.json identifica o ZIP por SHA-256, a revisão do Git e as versões de Python e das bibliotecas principais. Foi usado um ambiente virtual com acesso aos pacotes do sistema e as versões fixadas nos dois arquivos de dependências do projeto.
- 01_integracao.txt registra o comando, a saída mensal e o código de saída do processamento dos originais.
- 02_especialidades.txt registra o recálculo da produção por especialidade.
- 03_comparacao.txt registra o confronto dos cinco CSV reconstruídos com os CSV da revisão avaliada. A comparação considera cabeçalhos, ordem e conteúdo dos campos. Os hashes identificam os bytes dos DBC de entrada.
- 04_regressao_detalhada.txt mostra os sete casos de regressão individualmente. Os dados controlados de alguns casos provocam falhas deliberadas para exercitar os controles.
- 05_aplicacao_e_tabnet.txt registra o verificador da aplicação, os testes de filtros, P2, especialidades, a regressão e a conciliação mensal com as exportações preservadas. Os testes de interface usam AppTest. Avisos da biblioteca aparecem junto à saída dos scripts.
- resultado.json resume a conservação interna. conservacao.csv, hashes.csv e mensal.csv são saídas desta execução. O campo histórico “tabnet” em mensal.csv pertence à etapa de integração. O resultado da conciliação é produzido e conferido separadamente em verificar.py.

Os horários dos logs da reexecução em Linux estão registrados em UTC. A [verificação posterior no Windows](../verificacao_windows.txt) documenta a execução de 26/11/2026. A [configuração do computador utilizado nos testes iniciais](ambiente_windows_hardware.png) e o [registro das exportações TABNET](tabnet_datas_modificacao_exportacoes.png) complementam a documentação dos ambientes e das fontes.

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

## Ambiente Windows — desenvolvimento e testes iniciais

Windows 11 Home 25H2, sistema de 64 bits e processador x64. AMD Ryzen 5 5600 (seis núcleos, 3,50 GHz), 16 GB de RAM e NVIDIA GeForce RTX 3060 com 12 GB. Esse foi o ambiente utilizado por Maurício Rafael Oliveira da Silva durante a implementação e os testes iniciais. A reexecução em Linux corresponde à etapa complementar de verificação da reprodutibilidade.

## Registro das exportações TABNET

As exportações utilizadas na comparação externa estão preservadas no repositório. Os metadados de modificação registrados no Explorador do Windows correspondem a 23/11/2026, às 16h54, para a [exportação mensal](../../conciliacao/dados/sih_cnv_nidf165441138_0_247_22.csv), e às 20h12 para a [exportação por estabelecimento](../../conciliacao/maio/sih_cnv_nidf201212138_0_247_22.csv).
