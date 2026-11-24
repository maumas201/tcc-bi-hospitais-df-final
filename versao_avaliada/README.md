# Produção hospitalar do SUS no Distrito Federal
Aplicação Streamlit sobre agregados de junho/2025 a junho/2026. Uma linha de produção integrada corresponde a um código CNES em uma competência de processamento. A série tem 427 dessas combinações.
## Executar a aplicação
Extraia o projeto e abra o PowerShell na pasta de app.py. Use Python 3.12.
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m streamlit run app.py
```
## Repetir as conferências
```powershell
.\.venv\Scripts\python conferir_app.py
.\.venv\Scripts\python testar_p2.py
.\.venv\Scripts\python conferir_visual.py
.\.venv\Scripts\python conciliacao/importar_tabnet.py
```
Consulte [a documentação do código e dos dados](docs/implementacao.md) e [a descrição acadêmica da interface](docs/texto_TCC.md). Os registros de execução e as capturas estão em evidencias/. A aplicação abre com os CSV distribuídos e permite exportar a tabela filtrada de estabelecimentos.

## Versão avaliada e evidências
[Visão geral do DF](evidencias/DF_13_competencias.png) · [Hospital da Região Leste, P2 e especialidades](evidencias/P2_trimestre_especialidades.png) · [Conciliação financeira](evidencias/TABNET_valor.png)

Para repetir todas as conferências da aplicação e da comparação externa mensal em uma instalação nova, execute:
```powershell
.\.venv\Scripts\python verificar.py
```
A reexecução integral com os originais preservados reproduziu as tabelas mensal, painel, conservação, hashes e especialidades. Consulte [o resultado](evidencias/reconstrucao_DBC.txt) e [o procedimento](docs/reproducao.md).
