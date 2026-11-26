# Produção hospitalar do SUS no Distrito Federal

Protótipo de Business Intelligence que integra registros de autorizações de internação hospitalar (AIH) do SIH/SUS e cadastros de estabelecimentos e leitos do CNES. O painel permite consultar a produção por hospital e mês de processamento, examinar os leitos cadastrados e conferir os indicadores com os arquivos de origem. A versão avaliada abrange junho de 2025 a junho de 2026.

**TCC de Sistemas de Informação — UDF**  
**Título** — Integração de dados do SIH/SUS e do CNES no Distrito Federal: desenvolvimento e avaliação técnica de um protótipo de Business Intelligence para análise da produção hospitalar e dos leitos cadastrados.

| Autores | Contribuições |
|---|---|
| Maurício Rafael Oliveira da Silva | Implementação do código, testes, pesquisa de tecnologias e pesquisa metodológica. |
| Gabriel Silva dos Santos | Pesquisa de trabalhos correlatos, produção e revisão do texto e pesquisa metodológica. |

## Demonstração

![Visão geral do Distrito Federal com a produção e o valor aprovado por competência](docs/imagens/01_visao_geral.png)

[Assistir ou baixar a demonstração do painel (MP4, 4 min 13 s)](docs/video/demonstracao.mp4) · [Galeria com as seis capturas e seus filtros](docs/galeria.md)

## Executar e verificar no Windows

Com Git e Python 3.12 instalados, abra o PowerShell em uma pasta de trabalho e execute os comandos abaixo. Quem já tem o clone pode começar na pasta `versao_avaliada` do repositório.

```powershell
git clone https://github.com/maumas201/tcc-bi-hospitais-df-final.git
cd tcc-bi-hospitais-df-final/versao_avaliada
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe verificar.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

O painel abre com os CSV agregados distribuídos. Para repetir o processamento desde os DBC, consulte o [procedimento de reconstrução](versao_avaliada/docs/reproducao.md) e o [manifesto dos arquivos de origem](versao_avaliada/processamento/manifesto_publico.csv).

## Tecnologias da versão avaliada

| Componente | Versão | Responsabilidade |
|---|---|---|
| Python | 3.12.10 na verificação Windows | Processamento, execução do painel e testes |
| pandas | 2.3.3 | Leitura, agregação e integração das tabelas |
| pyreaddbc e dbfread | 2.0.4 e 2.0.7 | Conversão dos arquivos DBC e leitura dos registros DBF |
| Streamlit | 1.50.0 | Interface, filtros e testes da aplicação com AppTest |
| Altair | 5.5.0 | Visualizações do painel |

[Dependências do painel](versao_avaliada/requirements.txt) · [Dependências do processamento](versao_avaliada/processamento/requirements.txt) · [Documentação da implementação](versao_avaliada/docs/implementacao.md)

## Como conferir os resultados

| Verificação | Resultado da versão avaliada | Evidência |
|---|---|---|
| Conservação após integrar SIH e CNES | 427 pares de estabelecimento e competência conferidos, com a mesma contagem de registros e o mesmo valor aprovado antes e depois da integração | [CSV por chave](versao_avaliada/dados/conservacao.csv) |
| Reconstrução a partir da coleta preservada | Cinco tabelas reproduzidas a partir dos arquivos originais | [Comparação das tabelas](versao_avaliada/evidencias/evidencias_reexecucao/03_comparacao.txt) |
| Regressão | Sete testes aprovados | [Casos e resultados](versao_avaliada/evidencias/evidencias_reexecucao/04_regressao_detalhada.txt) |
| Aplicação e cenário P2 | Verificação dos filtros, especialidades e razão entre registros de AIH e leitos SUS | [Execução Windows](versao_avaliada/evidencias/verificacao_windows.txt) · [Resultado do P2](versao_avaliada/resultado_p2.txt) |
| Comparação externa | A tabela mensal permite identificar as competências com diferenças entre o painel e a consulta TABNET preservada | [Exportações e comparação](versao_avaliada/conciliacao/) |

A conferência interna compara o painel aos arquivos RD da coleta. A comparação com o TABNET usa uma exportação externa e tem resultado próprio. As evidências disponíveis permitem quantificar as diferenças observadas. Sua causa permanece indeterminada.

[Guia da aplicação](versao_avaliada/README.md) · [Ambiente e logs da reexecução](versao_avaliada/evidencias/evidencias_reexecucao/LEIA-ME.md) · [Demais evidências](versao_avaliada/evidencias/)
