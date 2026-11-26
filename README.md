# Business Intelligence na gestão hospitalar pública do Distrito Federal

Repositório da versão avaliada do TCC II, com aplicação Streamlit, dados públicos agregados do SIH-SUS e CNES, processamento e evidências de verificação. O recorte corresponde a 13 competências, de junho de 2025 a junho de 2026.

**TCC de Sistemas de Informação — UDF**  
**Título:** Integração de dados do SIH/SUS e do CNES no Distrito Federal: desenvolvimento e avaliação técnica de um protótipo de Business Intelligence para análise da produção hospitalar e dos leitos cadastrados.

| Autores | Contribuições |
|---|---|
| Maurício Rafael Oliveira da Silva | Implementação do código, testes, pesquisa de tecnologias e pesquisa metodológica. |
| Gabriel Silva dos Santos | Pesquisa de trabalhos correlatos, produção e revisão do texto e pesquisa metodológica. |

## Visão do painel

![Visão geral do Distrito Federal — 13 competências](versao_avaliada/evidencias/DF_13_competencias.png)

## Execução

Com Python 3.12, abra o PowerShell na raiz deste repositório:

```powershell
cd versao_avaliada
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python verificar.py
.\.venv\Scripts\python -m streamlit run app.py
```

## Tecnologias da versão avaliada

| Componente | Versão | Responsabilidade |
|---|---|---|
| Python | 3.12.10 na verificação Windows | Processamento, painel e testes |
| pandas | 2.3.3 | Leitura, agregação e integração de tabelas |
| pyreaddbc e dbfread | 2.0.4 e 2.0.7 | Conversão DBC e leitura DBF |
| Streamlit | 1.50.0 | Interface, filtros e testes AppTest |
| Altair | 5.5.0 | Visualizações |

[Dependências do painel](versao_avaliada/requirements.txt) · [Dependências do processamento](versao_avaliada/processamento/requirements.txt)

## Conferência dos resultados

A conferência interna compara os agregados do painel com os arquivos RD da coleta preservada. A comparação externa com a exportação TABNET é uma etapa distinta; as diferenças observadas não têm causa determinada.

A reexecução documentada corresponde ao commit [09f2817](https://github.com/maumas201/tcc-bi-hospitais-df-final/tree/09f2817ca8a9d60fe1cfa21656f9b7f8a931a76b). Veja o [ambiente](versao_avaliada/evidencias/evidencias_reexecucao/ambiente.json), a [comparação das tabelas reconstruídas](versao_avaliada/evidencias/evidencias_reexecucao/03_comparacao.txt) e os [sete testes de regressão](versao_avaliada/evidencias/evidencias_reexecucao/04_regressao_detalhada.txt).

## Documentação e evidências

- [README da aplicação](versao_avaliada/README.md)
- [Implementação e dados](versao_avaliada/docs/implementacao.md)
- [Reconstrução a partir dos arquivos originais](versao_avaliada/docs/reproducao.md)
- [Manifesto dos arquivos públicos](versao_avaliada/processamento/manifesto_publico.csv)
- [Evidências da aplicação e testes](versao_avaliada/evidencias/)
- [Conciliação TABNET](versao_avaliada/conciliacao/)

O painel usa os CSVs agregados distribuídos neste repositório. A reconstrução integral exige os arquivos originais, conforme o procedimento documentado. Os indicadores são descritivos e não substituem sistemas oficiais nem avaliações clínicas ou institucionais.
