# Declaração de uso de inteligência artificial

## Aulas 21 e 22

**Ferramenta utilizada:** ChatGPT (OpenAI).

**Aplicação:** auxílio na estruturação do `app.py` em Streamlit, construção dos filtros, matriz de correlação, histograma, indicadores, documentação das métricas, identidade visual e rascunho da segunda aba.

**Conteúdo aceito/adaptado:** a organização em sidebar e duas abas, uso de `st.cache_data`, seleção de variáveis, intervalo numérico e indicadores calculados dinamicamente a partir dos dados da EDA.

## Aula 23 (finalização e deploy)

**Ferramenta utilizada:** Claude Code (Anthropic), com a Agent Skill oficial `developing-with-streamlit` (instalada junto com o pacote `streamlit`).

**Aplicação:**
- preparo do dataset tratado: tratamento do texto `(null)` como ausente, extração do ano a partir de `id_unico`, remoção da coluna redundante `feridos` e exportação em Parquet para caber no GitHub e na memória do Streamlit Community Cloud;
- célula nova no notebook para salvar os dataframes original e tratado;
- Dashboard 2 com 4 visuais em Altair e seleção cruzada por UF, filtro por período e ajustes de API (`width="stretch"` no lugar de `use_container_width`, que foi descontinuado);
- rascunho do Dashboard 1 (`entregas/rascunho-dashboard1.jpg`), atualização do rascunho do Dashboard 2, README e esta declaração.

**Validação realizada:** o app foi executado localmente com a base completa (1.851.865 registros). Foram testados: 0, 1 e 2+ variáveis na correlação; filtros por UF, classificação, período e intervalo; troca da variável de distribuição; e o clique em uma UF no Dashboard 2 filtrando os demais gráficos. Os KPIs foram conferidos com cálculos diretos em pandas.

**Motivo do uso:** acelerar o desenvolvimento técnico sem substituir a interpretação e a validação crítica dos resultados da análise.
