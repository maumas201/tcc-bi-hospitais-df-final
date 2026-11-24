# Código, dados e reprodução
## Interface
Comando de entrada: streamlit run app.py. ler_csv preserva CNES, competência e ESPEC como texto e guarda as leituras em cache por caminho e separador. app.py seleciona o período, depois a unidade. O recorte alimenta as duas primeiras abas. A conservação interna acompanha a unidade. A referência mensal externa acompanha somente o período, pois abrange o DF.
|Arquivo|Responsabilidade e saída|
|---|---|
|app.py|Leitura dos CSV, filtros, cartões, rankings, tabelas, exportação e apresentação das diferenças externas.|
|graficos.py|Recebe uma série indexada por competência; ordenação cronológica, rótulos MM/AAAA, linhas com pontos, escala própria por medida. A moeda entra em centavos e o eixo mostra milhões de reais. A dica exibe o valor em reais e centavos. Uma lacuna interrompe a linha. Para um mês a tela apresenta os cartões.|
|indicador.py|Formata registros de AIH / leitos SUS de uma unidade em um mês. Explicita os motivos de indisponibilidade quando o denominador está ausente ou vale zero.|
|conferir_app.py, conferir_visual.py e testar_p2.py|Exercitam a aplicação com AppTest. Conferem totais contra o controle, estados dos filtros, conciliação, integridade, nomes, contagens e casos de fronteira da razão.|
## Arquivos consumidos
painel.csv contém medidas por CNES e mês. conservacao.csv registra contagens e centavos antes e depois da junção. hashes.csv contém os resumos SHA-256 da execução. nomes_consultados.csv associa rótulos auxiliares aos códigos CNES. especialidades.csv contém contagens do RD por CNES, competência e ESPEC. dominio_espec.csv fornece uma descrição por código. Um código sem descrição continua visível. comparacao_tabnet.csv preserva referências e diferenças em registros e centavos.
## Origem do domínio ESPEC
Para as categorias 01 a 09, ver Ministério da Saúde, Manual do SIH/SUS, seção 9, Especialidade. Para 87, ver a ficha RIPSA que explicita a seleção por ESPEC. A tabela traduz o código da AIH. O quantitativo de leitos vem do CNES/LT.
- https://bvsms.saude.gov.br/bvs/publicacoes/07_0066_M.pdf
- https://app.wiki.saude.es.gov.br/vigilancia/sim/indicadores_ripsa_2026.pdf
## Processamento da série
Em processamento/, serie.py baixa RD/ST/LT e cria as fichas e o manifesto de coleta. analisar.py verifica os hashes, converte DBC para DBF, lê campos selecionados e produz painel.csv, mensal.csv, hashes.csv e conservacao.csv nessa pasta. scripts/conferir_dbf.py lê a estrutura DBF; tccbi/core.py prepara as fontes e integra os agregados; tccbi/auditoria.py confronta contagens e centavos por chave. O controle do piloto fica em evidencias/junho/ dentro de processamento/.
Para reconstruir a partir do serviço do DATASUS, abra o PowerShell na raiz deste projeto:
```powershell
.\.venv\Scripts\python -m pip install -r processamento/requirements.txt
Push-Location processamento
..\.venv\Scripts\python serie.py baixar
..\.venv\Scripts\python analisar.py .
..\.venv\Scripts\python -m unittest discover -s tests
Pop-Location
```
A coleta requer acesso ao servidor FTP. Uma coleta posterior pode obter outros bytes. Antes de substituir os agregados, compare o manifesto e as saídas com os arquivos da execução avaliada. Para reconstruir especialidades.csv com os originais preservados, execute processamento/especialidades.py passando o caminho do ZIP de resultados que contém coleta_df/manifesto.csv e os DBC em coleta_df/AAAAMM/. O script confere as contagens contra dados/painel.csv e grava dados/especialidades.csv.
## Referência externa
conciliacao/importar_tabnet.py lê a exportação mensal em conciliacao/dados, verifica subtotais e seleciona 13 competências. comparar_tabnet.py confronta o recorte com mensal.csv e escreve conciliacao/comparacao_tabnet.csv. Compare com dados/comparacao_tabnet.csv. A exportação por estabelecimento de maio/2026 está em conciliacao/maio/. O sinal da diferença é painel menos TABNET.
## Versionamento
Esta pasta pode ser incorporada como versao_avaliada/ no repositório existente. O README da raiz do repositório deve apontar para seu README. Preserve os caminhos relativos dentro dela. Versione scripts, requirements, dados agregados, documentação e evidências selecionadas. Mantenha a coleta com registros individuais e os ambientes virtuais fora do Git. Revise git status antes do commit.
