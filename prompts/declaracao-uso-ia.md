# Declaração de Uso de IA

**Nome:** Pedro Henrique Martins Cavalcanti
**Data:** 29/10/2026

## Ferramenta

- **Aulas 21 e 22:** ChatGPT (OpenAI).
- **Aula 23:** Claude Code (Anthropic, modelo Claude Opus 5.5), com a skill oficial `developing-with-streamlit`, que vem junto com o pacote `streamlit`.

## Prompt usado

**Aulas 21 e 22 (ChatGPT):** pedidos para estruturar o `app.py` em Streamlit a partir do rascunho do layout (sidebar com filtros, matriz de correlação, histograma), propor KPIs para o Dashboard 2 e redigir a justificativa das métricas. O template de prompt preenchido para este projeto está em [layout-skeleton-prompt.md](layout-skeleton-prompt.md).

**Aula 23 (Claude Code):** enviei os PDFs das Aulas 21, 22 e 23 e os arquivos do projeto, com os pedidos:

> "preciso que vc faça oq ta se pedindo passo a passo, eu ja comecei"

> "faca tudo pra mim sem precisar pedi permissão"

Depois pedi para conferir o repositório-modelo da professora (`mfal-school/AVD-20262-pratica-streamlit`) e ajustar o projeto ao `ROTEIRO.md`.

## O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:**
  - organização em sidebar + duas abas (`st.tabs`), uso de `@st.cache_data` em `src/data_loader.py` e indicadores recalculados a partir dos filtros;
  - Dashboard 2 em Altair com seleção cruzada: clicar numa UF filtra os outros gráficos e, via `on_select="rerun"`, também os KPIs (exemplo 3 do `ALTAIR-CROSSFILTER.md`);
  - tratamento do dataset: o texto `(null)` da base passa a valor ausente, o ano é extraído de `id_unico` e a coluna `feridos` é removida por ser sempre `feridos_leves + feridos_graves` (o app recalcula).
- **Modificado:**
  - o dado tratado é versionado em **Parquet** (`data/clean/dataset.parquet`, ~7 MB) e não em CSV: o CSV tratado tem ~104 MB, acima do limite de 100 MB do GitHub, e ocuparia ~600 MB de memória no Streamlit Cloud (limite de ~1 GB). O README do modelo prevê essa alternativa;
  - o Dashboard 1 saiu do Plotly e passou para o Altair, que o roteiro indica como preferível;
  - o histograma mostra uma barra por valor (as variáveis são contagens) e junta a cauda rara numa barra "N+", porque com faixas automáticas quase tudo caía na primeira barra.
- **Rejeitado:**
  - mandar os ~1,85 milhão de linhas direto para o Altair: os gráficos recebem tabelas já agregadas no pandas, para o app continuar rápido;
  - colocar o Claude como coautor dos commits.

**Validação:** o app foi executado com a base completa (1.851.865 registros). Testei 0, 1 e 2+ variáveis na correlação, Pearson e Spearman, filtros por período, UF, classificação e intervalo, e o clique numa UF no Dashboard 2. Os KPIs foram conferidos com cálculos diretos em pandas (ex.: PE = 74.044 acidentes, 6,3% com óbito).
