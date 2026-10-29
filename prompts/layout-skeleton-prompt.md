# Template: rascunho de layout → esqueleto do app

Preencha cada bloco e envie à ferramenta de IA.

## Contexto

Sou aluno de Análise e Visualização de Dados (CESAR School, 2026.2). Projeto: dois dashboards em Streamlit a partir da minha EDA de acidentes em rodovias federais brasileiras (PRF/Kaggle, 2007–2020, ~1,85 milhão de registros). O Dashboard 1 mostra correlação e distribuição das variáveis quantitativas; o Dashboard 2 mostra KPIs de frequência e gravidade.

## Entrada

- Rascunhos: `entregas/rascunho-dashboard1.jpg` e `entregas/rascunho-dashboard2.jpg` (anexados).
- Colunas do dataset tratado: `ano`, `uf`, `classificacao_acidente`, `fase_dia`, `condicao_metereologica`, `pessoas`, `mortos`, `feridos_leves`, `feridos_graves`, `ilesos`, `ignorados`, `veiculos`.
- Perguntas: como as contagens de vítimas se relacionam entre si? Como estão distribuídas? Onde se concentram os acidentes e qual a proporção de acidentes com óbito?
- Layout: sidebar à esquerda com filtros (período, UF, classificação, variáveis, intervalo); aba 1 com heatmap de correlação e histograma lado a lado; aba 2 com 5 métricas no topo e gráficos abaixo.

## Restrições

- Streamlit + Altair; editar só o `app.py`; carregar dados via `src/data_loader.py`.
- Gerar só o esqueleto estrutural, com placeholders no lugar dos gráficos.
- Não usar caminhos absolutos nem CSS customizado.

## Formato de saída

Um único `app.py` completo, pronto para `streamlit run app.py`, com comentários `# TODO` onde entram os gráficos.
