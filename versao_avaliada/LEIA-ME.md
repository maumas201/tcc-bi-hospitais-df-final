# Painel hospitalar do Distrito Federal
Extraia a pasta e abra o PowerShell nela. Com Python 3.12 instalado, execute:
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m streamlit run app.py
```
Os CSVs agregados correspondem à versão avaliada da integração SIH/SUS e CNES. O código de processamento dos DBC está disponível em [processamento/](processamento/), e o procedimento de reconstrução está descrito na [documentação técnica](docs/reproducao.md). Esta versão apresenta a conciliação mensal do DF. A investigação por estabelecimento em maio/2026 é uma evidência separada.

## Conferência da versão
Para repetir o teste automatizado, execute no PowerShell da pasta:
```powershell
.\.venv\Scripts\python conferir_app.py
```
Na aba Qualidade e rastreabilidade, "RD antes da integração" vem dos totais por unidade e mês apurados nos arquivos SIH/RD baixados. "Painel" é recalculado a partir da tabela integrada. A comparação externa usa a exportação mensal do TABNET para o DF. A conferência SHA-256 usa o manifesto local da coleta.

## Cenário P2 · coordenação da unidade
Na aba Estabelecimentos, selecione CNES 2645157 e outubro de 2025. Confira 1.138 registros, 246 leitos SUS e 4,63 registros por leito SUS. Até dezembro, confira 4,63, 4,45 e 5,54 nas linhas mensais. O teste automatizado verifica os cartões e a tabela. Duas cópias temporárias independentes exercitam os casos de zero e ausência de leitos. Execute:
```powershell
.\.venv\Scripts\python testar_p2.py
```
