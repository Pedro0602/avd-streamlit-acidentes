# 🚗 Acidentes em rodovias federais — Dashboards em Streamlit

Projeto das Aulas 21, 22 e 23 de **Análise e Visualização de Dados** (CESAR School, 2026.2), feito a partir do repositório-modelo [mfal-school/AVD-20262-pratica-streamlit](https://github.com/mfal-school/AVD-20262-pratica-streamlit).
Dois dashboards interativos sobre os acidentes registrados pela PRF em rodovias federais brasileiras (2007–2020, ~1,85 milhão de registros), construídos a partir da EDA da Aula 11:

- **Dashboard 1** = correlação + distribuição das variáveis quantitativas
- **Dashboard 2** = KPIs

**Link do app (Aula 23):** https://avd-acidentes-rodovias.streamlit.app

## O que tem no app

| Aba | Conteúdo |
|---|---|
| **Dashboard 1 — Correlação e distribuição** | Heatmap de correlação (Pearson ou Spearman) das variáveis escolhidas e histograma da variável selecionada, com opção de limitar ao percentil 99 |
| **Dashboard 2 — Indicadores** | 5 KPIs (acidentes, pessoas, óbitos, feridos, % de acidentes com óbito) e 4 gráficos Altair ligados: **clicar numa UF** filtra a evolução anual, a classificação, a % de óbitos por fase do dia **e os KPIs** |

Os filtros da sidebar (período, UF, classificação e intervalo de valores) valem para as duas abas.

**Stack:** Python · Streamlit · pandas · Altair · PyArrow (Parquet).

## Estrutura

```
app.py                              # aplicação Streamlit (na raiz)
src/data_loader.py                  # leitura do dado tratado, com @st.cache_data
data/clean/dataset.parquet          # dataset tratado usado pelo app (versionado, ~7 MB)
data/raw/                           # dataset original (não versionado)
notebooks/eda.ipynb                 # EDA original da Aula 11
notebooks/eda-com-downloads.ipynb   # EDA + células finais que salvam data/raw e data/clean
notebooks/arquivo-eda-original.ipynb  # EDA da professora, mantida para consulta
scripts/preparar_dados.py           # alternativa ao notebook: baixa do Kaggle e gera data/
entregas/                           # rascunhos dos dashboards e justificativa das métricas
prompts/                            # declaração de uso de IA e template de prompt
.streamlit/config.toml              # identidade visual
```

## Setup

Requer **Python 3.11 a 3.15** (desenvolvido com 3.14).

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

No macOS/Linux: `python3 -m venv .venv` e `source .venv/bin/activate`.

## Dados: `data/raw` vs `data/clean`

- **Fonte:** [Kaggle — Acidentes em Rodovias Federais 2007–2020](https://www.kaggle.com/datasets/marcosfnlr/acidentes-em-rodovias-federais-20072020) (dados públicos da PRF, sem dados pessoais).
- `data/raw/dataset.csv`: base original (~385 MB). Não vai para o Git.
- `data/clean/`: base tratada, gerada pela última célula de `notebooks/eda-com-downloads.ipynb` (ou por `python scripts/preparar_dados.py`).
- **Por que Parquet:** o CSV tratado tem ~104 MB, acima do limite de 100 MB por arquivo do GitHub, e ocuparia ~600 MB de memória no Streamlit Cloud (limite de ~1 GB). Como o README do modelo sugere, o dado tratado é versionado em Parquet (`data/clean/dataset.parquet`, ~7 MB, ~45 MB em memória). O app lê o Parquet e só usa o CSV se ele não existir.

## Deploy (Streamlit Community Cloud)

Repositório `Pedro0602/avd-streamlit-acidentes`, branch `main`, arquivo `app.py`, Python 3.14. Cada `git push` na `main` atualiza o app.

## Entregas e uso de IA

- [entregas/](entregas): `rascunho-dashboard1.jpg`, `rascunho-dashboard2.jpg` e [justificativa-metricas.md](entregas/justificativa-metricas.md).
- [prompts/declaracao-uso-ia.md](prompts/declaracao-uso-ia.md): ferramentas, prompts e o que foi aceito, modificado ou rejeitado.

## Cuidados de interpretação

A base contém acidentes **registrados**, sem fluxo de veículos nem quilômetros rodados: mais acidentes não significa necessariamente maior risco. Correlação não implica causalidade.
