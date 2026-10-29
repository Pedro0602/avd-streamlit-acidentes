import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from src.data_loader import VARS_QUANT, load_data

st.set_page_config(page_title="Painel de Acidentes | AVD", page_icon="🚗", layout="wide")

LARANJA = "#E86520"
AZUL = "#28537B"
CINZA = "#C9D3DD"


def formatar(valor):
    """Número no padrão brasileiro (1.234.567)."""
    return f"{valor:,.0f}".replace(",", ".") if pd.notna(valor) else "N/D"


st.title("🚗 Acidentes em rodovias federais")
st.caption("Análise e Visualização de Dados • Aulas 21 a 23 • EDA da base PRF/Kaggle (2007–2020)")

try:
    df = load_data()
except FileNotFoundError:
    st.error("O dataset tratado ainda não está em data/clean/.", title="Dados não encontrados")
    st.info("Rode a última célula de notebooks/eda-com-downloads.ipynb ou: python scripts/preparar_dados.py")
    st.stop()

quant = [c for c in VARS_QUANT if c in df.columns]

# ----------------------------- Sidebar: filtros -----------------------------
st.sidebar.header("🎛️ Filtros da análise")
mascara = pd.Series(True, index=df.index)
if "ano" in df:
    ano_min, ano_max = int(df["ano"].min()), int(df["ano"].max())
    anos = st.sidebar.slider("Período (ano)", ano_min, ano_max, (ano_min, ano_max))
    mascara &= df["ano"].between(*anos)
if "uf" in df:
    estados = st.sidebar.multiselect("Unidades federativas", sorted(df["uf"].dropna().unique()), placeholder="Todas")
    if estados:
        mascara &= df["uf"].isin(estados)
if "classificacao_acidente" in df:
    classes = st.sidebar.multiselect(
        "Classificação dos acidentes", sorted(df["classificacao_acidente"].dropna().unique()), placeholder="Todas"
    )
    if classes:
        mascara &= df["classificacao_acidente"].isin(classes)

st.sidebar.subheader("Dashboard 1")
selecionadas = st.sidebar.multiselect("Variáveis para correlação", quant, default=quant[:4])
metodo = st.sidebar.segmented_control("Método da correlação", ["Pearson", "Spearman"], default="Pearson")
variavel = st.sidebar.selectbox("Variável para distribuição", quant)
serie = df.loc[mascara, variavel].dropna()
if serie.empty:
    st.warning("Não há valores disponíveis com os filtros escolhidos.")
    st.stop()
minimo, maximo = float(serie.min()), float(serie.max())
if minimo < maximo:
    a, b = st.sidebar.slider(f"Intervalo de {variavel}", min_value=minimo, max_value=maximo,
                             value=(minimo, maximo), step=1.0)
    mascara &= df[variavel].between(a, b)
else:
    st.sidebar.caption("A variável selecionada só possui um valor.")
st.sidebar.caption("Os filtros afetam os dois dashboards e seus indicadores.")

filtrado = df[mascara]
if filtrado.empty:
    st.warning("Não há acidentes para essa combinação de filtros. Altere a seleção.")
    st.stop()

tab1, tab2 = st.tabs(["📊 Dashboard 1 — Correlação e distribuição", "📈 Dashboard 2 — Indicadores"])

# ----------------------------- Dashboard 1 -----------------------------
with tab1:
    st.subheader("Relação entre variáveis e distribuição dos acidentes")
    st.caption(f"{formatar(len(filtrado))} de {formatar(len(df))} acidentes dentro dos filtros escolhidos.")
    col_corr, col_dist = st.columns([1.1, 1], gap="large")

    with col_corr:
        st.markdown(f"**Matriz de correlação ({metodo or 'Pearson'})**")
        if len(selecionadas) < 2:
            st.info("Selecione ao menos duas variáveis quantitativas para visualizar a correlação.")
        elif len(filtrado) < 30:
            st.warning("Poucos acidentes nos filtros escolhidos para calcular a correlação.")
        else:
            base_corr = filtrado[selecionadas]
            if metodo == "Spearman" and len(base_corr) > 300_000:
                # Spearman ordena todos os valores: amostra reprodutível, como na EDA
                base_corr = base_corr.sample(300_000, random_state=42)
            matriz = base_corr.corr(method=(metodo or "Pearson").lower())
            # Só o triângulo inferior, sem a diagonal (a matriz é simétrica)
            ordem = {v: i for i, v in enumerate(selecionadas)}
            corr = (matriz.rename_axis(index="var_y", columns="var_x").stack(future_stack=True)
                    .rename("correlacao").reset_index())
            corr = corr[corr["var_y"].map(ordem) > corr["var_x"].map(ordem)].dropna()
            if corr.empty:
                st.warning("Correlação indefinida: alguma variável ficou constante com os filtros atuais.")
            else:
                base = alt.Chart(corr).encode(
                    x=alt.X("var_x:N", title=None, sort=selecionadas[:-1], axis=alt.Axis(labelAngle=-30)),
                    y=alt.Y("var_y:N", title=None, sort=selecionadas[1:]),
                )
                heatmap = base.mark_rect().encode(
                    color=alt.Color("correlacao:Q", title="r",
                                    scale=alt.Scale(scheme="redblue", domain=[-1, 1], reverse=True)),
                    tooltip=[alt.Tooltip("var_x:N", title="Variável"), alt.Tooltip("var_y:N", title="Variável"),
                             alt.Tooltip("correlacao:Q", title="r", format=".2f")],
                )
                valores = base.mark_text(fontSize=15).encode(
                    text=alt.Text("correlacao:Q", format=".2f"),
                    color=alt.condition("abs(datum.correlacao) > 0.5", alt.value("white"), alt.value("black")),
                )
                st.altair_chart((heatmap + valores).properties(height=420), width="stretch",
                                alt=f"Mapa de calor da correlação de {metodo} entre as variáveis selecionadas")

    with col_dist:
        st.markdown(f"**Distribuição de `{variavel}`**")
        p99 = st.toggle("Limitar visualização ao percentil 99 (sem alterar indicadores)", value=False)
        valores_var = filtrado[variavel].dropna()
        if p99:
            valores_var = valores_var[valores_var <= valores_var.quantile(0.99)]
        if valores_var.empty:
            st.info("Sem valores válidos para gerar o histograma.")
        else:
            # As variáveis são contagens inteiras e muito assimétricas: uma barra por valor (0, 1, 2...)
            # e a cauda rara (acima do percentil 99,5) junta numa última barra "N+".
            # A contagem é feita no pandas e o Altair recebe só a tabela resumida.
            corte = int(max(10, np.ceil(valores_var.quantile(0.995))))
            inteiros = valores_var.round().astype(int)
            rotulos = inteiros.where(inteiros <= corte, corte + 1)
            freq = rotulos.value_counts().sort_index().rename_axis("valor").reset_index(name="acidentes")
            freq["faixa"] = freq["valor"].astype(str)
            freq.loc[freq["valor"] > corte, "faixa"] = f"{corte + 1}+"
            barras = alt.Chart(freq).mark_bar(color=LARANJA).encode(
                x=alt.X("faixa:N", title=variavel, sort=freq["faixa"].tolist(), axis=alt.Axis(labelAngle=0)),
                y=alt.Y("acidentes:Q", title="Acidentes"),
                tooltip=[alt.Tooltip("faixa:N", title=variavel),
                         alt.Tooltip("acidentes:Q", title="Acidentes", format=",.0f")])
            st.altair_chart(barras.properties(height=420), width="stretch",
                            alt=f"Histograma da variável {variavel}")
            st.caption(f"Média {valores_var.mean():.2f} • mediana {valores_var.median():.0f} • "
                       f"máximo {valores_var.max():.0f}")

    with st.expander("Estatísticas descritivas e interpretação"):
        st.dataframe(filtrado[quant].describe().T.round(2), width="stretch")
        st.caption("Correlação não implica causalidade. As variáveis são contagens por acidente, com forte assimetria "
                   "(muitos zeros); por isso o Spearman é oferecido como alternativa ao Pearson.")

# ----------------------------- Dashboard 2 -----------------------------
with tab2:
    st.subheader("Indicadores de frequência e gravidade")
    area_kpis = st.container()  # os KPIs são desenhados depois, já considerando o clique no gráfico
    st.markdown("**Clique em uma UF** para filtrar os KPIs e os outros gráficos "
                "(Shift + clique seleciona várias; clique duplo limpa).")

    grupos = [c for c in ["uf", "ano", "classificacao_acidente", "fase_dia"] if c in filtrado]
    ufs_clicadas = []
    if "uf" in grupos and "mortos" in filtrado:
        # Tabela agregada pequena (alguns milhares de linhas) em vez de ~1,85 milhão para o Altair
        agregado = (filtrado.assign(fatal=(filtrado["mortos"].fillna(0) > 0).astype("int32"))
                    .groupby(grupos, observed=True, dropna=False)
                    .agg(acidentes=("fatal", "size"), fatais=("fatal", "sum"))
                    .reset_index())
        for c in grupos:
            if c != "ano":
                agregado[c] = agregado[c].astype("string").fillna("Não informado")

        clique = alt.selection_point(name="clique_uf", fields=["uf"], on="click", clear="dblclick")
        base = alt.Chart(agregado)
        por_uf = (base.mark_bar(cornerRadiusEnd=3)
                  .encode(y=alt.Y("uf:N", sort="-x", title="UF"),
                          x=alt.X("sum(acidentes):Q", title="Acidentes registrados"),
                          color=alt.condition(clique, alt.value(AZUL), alt.value(CINZA)),
                          tooltip=[alt.Tooltip("uf:N", title="UF"),
                                   alt.Tooltip("sum(acidentes):Q", title="Acidentes", format=",.0f")])
                  .add_params(clique)
                  .properties(title="Acidentes por UF", width=260, height=640))
        visuais = []
        if "ano" in agregado:
            visuais.append(
                base.transform_filter(clique).mark_line(point=True, color=AZUL)
                .encode(x=alt.X("ano:O", title="Ano"),
                        y=alt.Y("sum(acidentes):Q", title="Acidentes registrados"),
                        tooltip=[alt.Tooltip("ano:O", title="Ano"),
                                 alt.Tooltip("sum(acidentes):Q", title="Acidentes", format=",.0f")])
                .properties(title="Evolução anual dos acidentes", width=460, height=180))
        if "classificacao_acidente" in agregado:
            visuais.append(
                base.transform_filter(clique).mark_bar(color=LARANJA)
                .encode(y=alt.Y("classificacao_acidente:N", sort="-x", title=None),
                        x=alt.X("sum(acidentes):Q", title="Acidentes registrados"),
                        tooltip=[alt.Tooltip("classificacao_acidente:N", title="Classificação"),
                                 alt.Tooltip("sum(acidentes):Q", title="Acidentes", format=",.0f")])
                .properties(title="Acidentes por classificação", width=460, height=150))
        if "fase_dia" in agregado:
            visuais.append(
                base.transform_filter(clique)
                .transform_aggregate(acidentes="sum(acidentes)", fatais="sum(fatais)", groupby=["fase_dia"])
                .transform_calculate(pct="datum.fatais / datum.acidentes")
                .mark_bar(color=LARANJA)
                .encode(y=alt.Y("fase_dia:N", sort="-x", title=None),
                        x=alt.X("pct:Q", title="% de acidentes com óbito", axis=alt.Axis(format="%")),
                        tooltip=[alt.Tooltip("fase_dia:N", title="Fase do dia"),
                                 alt.Tooltip("pct:Q", title="% com óbito", format=".1%"),
                                 alt.Tooltip("acidentes:Q", title="Acidentes", format=",.0f")])
                .properties(title="% de acidentes com óbito por fase do dia", width=460, height=150))

        grafico = alt.hconcat(por_uf, alt.vconcat(*visuais, spacing=28), spacing=40)
        # on_select="rerun": o clique volta para o Python e atualiza os KPIs (guia ALTAIR-CROSSFILTER, exemplo 3)
        evento = st.altair_chart(
            grafico.configure_view(stroke=None).configure_title(anchor="start", fontSize=15),
            key="dash2", on_select="rerun", width="content",
            alt="Acidentes por UF, evolução anual, classificação e % com óbito por fase do dia, ligados por clique na UF",
        )
        ufs_clicadas = [item["uf"] for item in evento.selection.get("clique_uf", []) if "uf" in item]
    else:
        st.info("Colunas UF e mortos são necessárias para os gráficos do Dashboard 2.")

    # KPIs: filtros da sidebar + UFs clicadas no gráfico
    recorte = filtrado[filtrado["uf"].isin(ufs_clicadas)] if ufs_clicadas else filtrado
    with area_kpis:
        if ufs_clicadas:
            st.caption("UF selecionada no gráfico: " + ", ".join(ufs_clicadas))
        n = len(recorte)
        fatais = (recorte["mortos"].fillna(0) > 0).sum() if "mortos" in recorte else np.nan
        kpis = [
            ("Acidentes registrados", formatar(n)),
            ("Pessoas envolvidas", formatar(recorte["pessoas"].sum()) if "pessoas" in recorte else "N/D"),
            ("Óbitos registrados", formatar(recorte["mortos"].sum()) if "mortos" in recorte else "N/D"),
            ("Feridos registrados", formatar(recorte["feridos"].sum()) if "feridos" in recorte else "N/D"),
            ("Acidentes com óbito", f"{fatais / n:.1%}".replace(".", ",") if n and pd.notna(fatais) else "N/D"),
        ]
        for coluna, (nome, valor) in zip(st.columns(5), kpis):
            coluna.metric(nome, valor, border=True)
        st.caption("Acidentes com óbito = registros com mortos > 0 ÷ acidentes no recorte. "
                   "Não representa risco por quilômetro rodado.")

    st.markdown("**Interpretação**: contagens absolutas descrevem o volume observado, não a probabilidade "
                "individual de acidente. A proporção de acidentes com óbito ajuda a comparar gravidade entre recortes.")

with st.expander("🔎 Conferir registros e qualidade dos dados"):
    st.write(f"Linhas filtradas: {formatar(len(filtrado))} | Variáveis quantitativas disponíveis: {len(quant)}")
    st.dataframe(filtrado.head(500), width="stretch")
