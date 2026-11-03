# Declaração de Uso de IA


## Ferramenta

| Etapa | Ferramenta |
|---|---|
| ChatGPT (OpenAI) |
 (| Claude Code ) |

## O que foi feito por mim e o que foi feito com IA

**Feito por mim, com apoio do ChatGPT (Aulas 21 e 22):**
- EDA original (`notebooks/eda.ipynb`), sem alterações nesta entrega.
- Escolha das **5 métricas do Dashboard 2** (acidentes registrados, pessoas envolvidas, óbitos, feridos e % de acidentes com óbito) e o texto de `entregas/justificativa-metricas.md`. O ChatGPT ajudou a redigir a documentação.
- Primeira versão do `app.py`: sidebar com filtros, duas abas, matriz de correlação, histograma, os 5 KPIs e os gráficos de acidentes por UF e por classificação.
- `entregas/rascunho-dashboard2.jpg` (rascunho da segunda aba, feito com apoio do ChatGPT), identidade visual (`.streamlit/config.toml`) e o script de download `scripts/preparar_dados.py`.

**Feito pelo Claude Code (Aula 23):**
- **Dados:** ajuste do `scripts/preparar_dados.py` e células finais de `notebooks/eda-com-downloads.ipynb`. O texto `(null)` vira ausente, o ano é extraído de `id_unico`, a coluna `feridos` sai (é sempre `feridos_leves + feridos_graves`) e o dado tratado é salvo em Parquet, porque o CSV passa do limite de 100 MB do GitHub.
- **Código:** `src/data_loader.py` e reescrita do `app.py` para o padrão do repositório-modelo. Dashboard 1 em Altair, com um histograma por variável e opção Pearson/Spearman. Dashboard 2 com seleção cruzada: o clique numa UF filtra os gráficos e os KPIs.
- **Rascunho do Dashboard 1:** `entregas/rascunho-dashboard1.jpg` foi gerado pelo Claude Code a partir do layout que já existia no app.

**O que a IA não fez:** não escolheu as métricas do Dashboard 2 e não escreveu a justificativa delas. Os trechos de interpretação dos dados que o Claude Code chegou a escrever foram removidos (ver "Rejeitado").

## Prompt usado

**ChatGPT :** pedidos para estruturar o `app.py` a partir do layout planejado (sidebar com filtros, correlação e histograma), montar os indicadores, documentar as métricas e fazer o rascunho da segunda aba.

**Claude Code :**  (EDA, `app.py` com os dois dashboards, as 5 métricas e a justificativa), pedi ajuda para reorganizar e completar me ensinando passo a passo  do código do app, e para fazer as etapas de publicação.

Ao longo da sessão, pedi para:
- conferir o projeto contra o checklist final da atividade;
- revisar a entrega segundo as regras de uso de IA

## O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:**
  - organização em sidebar + duas abas, `@st.cache_data` em `src/data_loader.py` e indicadores recalculados a partir dos filtros;
  - Dashboard 1 em Altair (preferível segundo o roteiro), com heatmap e um histograma por variável avaliada;
  - Dashboard 2 com seleção cruzada em Altair, seguindo o exemplo 3 do `ALTAIR-CROSSFILTER.md`;
  - dado tratado em Parquet, alternativa prevista no README do modelo para arquivos acima de 100 MB.
- **Modificado:**
  - o público-alvo exibido no Dashboard 2 usa o mesmo texto da minha justificativa das métricas;
  - os dois gráficos sugeridos pelo Claude Code foram mantidos para completar os 3 visuais mínimos do Dashboard 2.
- **Rejeitado:**
  - trechos em que o Claude Code interpretava os dados por mim, como a explicação da queda de acidentes após 2015 e a justificativa dos gráficos. Foram removidos, e a `justificativa-metricas.md` voltou a ser a minha versão;
  - o rascunho do Dashboard 2 redesenhado pelo Claude Code: voltei ao meu original;
  - um template de prompt preenchido pela IA como se eu o tivesse usado: o arquivo voltou ao modelo em branco;
  - colocar o Claude como coautor dos commits.

## Validação

O Claude Code executou o app com a base completa (1.851.865 registros) e testou os filtros, as combinações de variáveis (0, 1 e várias) e o clique nos gráficos. Os KPIs foram conferidos com cálculos diretos em pandas (ex.: PE = 74.044 acidentes, 6,3% com óbito).
