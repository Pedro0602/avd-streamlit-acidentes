# 🚗 Acidentes em rodovias federais — Dashboards em Streamlit

Projeto da disciplina **Análise e Visualização de Dados (AVD 2026.2)**, Aulas 21 a 23.
Dois dashboards interativos construídos a partir da EDA de acidentes registrados pela PRF em rodovias federais brasileiras (2007–2020, ~1,85 milhão de registros).

**🔗 App publicado:** COLOQUE_AQUI_O_LINK — ex.: `https://acidentes-rodovias.streamlit.app`

## O que tem no app

| Aba | Conteúdo |
|---|---|
| **Dashboard 1 — Correlação e distribuição** | Matriz de correlação (Pearson) das variáveis quantitativas escolhidas + histograma da variável selecionada, com opção de limitar ao percentil 99 |
| **Dashboard 2 — Indicadores** | 5 KPIs (acidentes, pessoas, óbitos, feridos, % de acidentes com óbito) + 4 gráficos Altair com **seleção cruzada**: clique numa UF para filtrar a evolução anual, a classificação e a % de óbitos por fase do dia |

Filtros na sidebar (valem para as duas abas): período, UF, classificação do acidente, variáveis da correlação, variável da distribuição e intervalo de valores.

**Stack:** Python · Streamlit · pandas · Altair · Plotly · PyArrow (Parquet).

## Estrutura do repositório

```
app.py                          # aplicação Streamlit (na raiz)
requirements.txt                # bibliotecas usadas
.streamlit/config.toml          # identidade visual (tema)
data/clean/dataset.parquet      # dataset tratado usado pelo app (versionado, ~7 MB)
notebooks/eda.ipynb             # EDA + exportação dos dataframes original e tratado
scripts/preparar_dados.py       # baixa a base do Kaggle e gera data/clean/
entregas/rascunho-dashboard1.jpg
entregas/rascunho-dashboard2.jpg
entregas/justificativa-metricas.md
prompts/declaracao-uso-ia.md
```

### Sobre o dataset
- Fonte: [Kaggle — Acidentes em Rodovias Federais 2007–2020](https://www.kaggle.com/datasets/marcosfnlr/acidentes-em-rodovias-federais-20072020) (dados da PRF).
- O CSV tratado (`data/clean/dataset.csv`) tem ~104 MB, acima do limite de **100 MB por arquivo do GitHub**, e ocuparia ~600 MB de memória no app.
  Por isso o app usa o **Parquet** (`data/clean/dataset.parquet`, ~7 MB, ~45 MB em memória), formato recomendado na Aula 23 para o limite de ~1 GB do plano gratuito. O CSV e a base original (`data/raw/`) ficam fora do Git e podem ser recriados com o script.

## Rodar localmente (Windows / PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

O Parquet já vem no repositório. Para recriar os arquivos de `data/` a partir do Kaggle (precisa de internet): `python scripts/preparar_dados.py`.

## Deploy no Streamlit Community Cloud

1. Acesse https://share.streamlit.io e entre com a **mesma conta do GitHub** do repositório.
2. **Create app → Deploy a public app from GitHub**.
3. Repository: este repositório · Branch: `main` · Main file path: `app.py`.
4. App URL: escolha um subdomínio (vira `https://<subdominio>.streamlit.app`).
5. **Advanced settings → Python 3.14** (mesma versão do `.venv` usado no desenvolvimento) → **Deploy**.
6. Copie o link e cole no topo deste README.

Cada `git push` na `main` atualiza o app automaticamente.

## Cuidados de interpretação
A base contém acidentes **registrados**, sem fluxo de veículos ou quilômetros rodados: mais acidentes não significa necessariamente maior risco. Correlação não implica causalidade.
