# Reproduzir a versão avaliada
## Consulta com os agregados distribuídos
Use Python 3.12 e siga a instalação no README ao lado de app.py. Execute verificar.py e depois inicie o Streamlit. A instalação da aplicação dispensa os DBC.
## Reconstrução integral
Use uma cópia limpa. Instale as dependências adicionais a partir de versao_avaliada e entre na pasta processamento:
```powershell
.\.venv\Scripts\python -m pip install -r processamento/requirements.txt
cd processamento
```
Para reproduzir com os originais preservados, extraia a pasta coleta_df/ do arquivo histórico TCC_resultados_e_dados_202506_202606.zip para dentro de processamento/. Ela inclui manifesto.csv, pastas AAAAMM, os DBC e as respectivas fichas JSON. Para realizar outra coleta, execute em uma pasta de trabalho nova:
```powershell
..\.venv\Scripts\python serie.py baixar
```
A partir de processamento/, execute com os arquivos e fichas disponíveis:
```powershell
..\.venv\Scripts\python analisar.py .
..\.venv\Scripts\python especialidades.py coleta_df --saida especialidades.csv
..\.venv\Scripts\python conferir_reconstrucao.py
```
A verificação confronta os 39 originais com os hashes públicos registrados para a versão avaliada. Depois compara cabeçalhos e valores dos cinco CSV, respeitando a ordem das linhas e aceitando finais de linha de Windows ou Linux. Uma revisão posterior da fonte pode produzir outros arquivos. Identifique a coleta correspondente antes de interpretar uma divergência. A reexecução complementar utilizou os arquivos originais preservados da coleta avaliada.
