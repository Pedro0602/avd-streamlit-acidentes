from pathlib import Path
import altair as alt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Painel de Acidentes | AVD', page_icon='🚗', layout='wide')

# Caminhos sempre relativos à pasta do app (funciona local e no Streamlit Community Cloud).
ROOT = Path(__file__).resolve().parent
PARQUET = ROOT / 'data' / 'clean' / 'dataset.parquet'
CSV = ROOT / 'data' / 'clean' / 'dataset.csv'
CANDIDATAS = ['pessoas', 'mortos', 'feridos_leves', 'feridos_graves', 'ilesos', 'ignorados', 'feridos', 'veiculos']
CATEGORIAS = ['uf', 'classificacao_acidente', 'fase_dia', 'condicao_metereologica']
LARANJA = '#E86520'
AZUL = '#28537B'
CINZA = '#C9D3DD'


@st.cache_data(show_spinner='Lendo dados tratados...')
def carregar_dados(arquivo, modificado):
    """Lê o dataset tratado uma única vez (cache) e prepara tipos leves para economizar memória."""
    if arquivo.endswith('.parquet'):
        df = pd.read_parquet(arquivo)
    else:
        df = pd.read_csv(arquivo, low_memory=False, dtype={c: 'category' for c in CATEGORIAS})
    # 'feridos' = feridos_leves + feridos_graves (relação conferida na EDA).
    if 'feridos' not in df and {'feridos_leves', 'feridos_graves'} <= set(df.columns):
        df['feridos'] = df['feridos_leves'] + df['feridos_graves']
    for col in CANDIDATAS:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('float32')
    for col in CATEGORIAS:
        if col in df:
            df[col] = df[col].astype('category')
    return df


def formatar(valor):
    return f'{valor:,.0f}'.replace(',', '.') if pd.notna(valor) else 'N/D'


st.title('🚗 Acidentes em rodovias federais')
st.caption('Análise e Visualização de Dados • Aulas 21 a 23 • EDA da base PRF/Kaggle (2007–2020)')

arquivo = PARQUET if PARQUET.is_file() else CSV
if not arquivo.is_file():
    st.error('O dataset tratado ainda não está em data/clean/.')
    st.info('Execute: python scripts/preparar_dados.py (precisa de internet no primeiro download).')
    st.stop()

df = carregar_dados(str(arquivo), arquivo.stat().st_mtime)
quant = [c for c in CANDIDATAS if c in df.columns]
if not quant:
    st.error('Não foram encontradas as variáveis quantitativas esperadas no dataset.')
    st.stop()

# ----------------------------- Filtros (sidebar) -----------------------------
st.sidebar.header('🎛️ Filtros da análise')
mascara = pd.Series(True, index=df.index)
if 'ano' in df:
    ano_min, ano_max = int(df['ano'].min()), int(df['ano'].max())
    anos = st.sidebar.slider('Período (ano)', ano_min, ano_max, (ano_min, ano_max))
    mascara &= df['ano'].between(*anos)
if 'uf' in df:
    estados = st.sidebar.multiselect('Unidades federativas', sorted(df['uf'].dropna().unique()),
                                     placeholder='Todas')
    if estados:
        mascara &= df['uf'].isin(estados)
if 'classificacao_acidente' in df:
    classes = st.sidebar.multiselect('Classificação dos acidentes',
                                     sorted(df['classificacao_acidente'].dropna().unique()), placeholder='Todas')
    if classes:
        mascara &= df['classificacao_acidente'].isin(classes)

selecionadas = st.sidebar.multiselect('Variáveis para correlação', quant, default=quant[:4])
variavel = st.sidebar.selectbox('Variável para distribuição', quant)
serie = df.loc[mascara, variavel].dropna()
if serie.empty:
    st.warning('Não há valores disponíveis com os filtros escolhidos.')
    st.stop()
minimo, maximo = float(serie.min()), float(serie.max())
if minimo < maximo:
    a, b = st.sidebar.slider('Intervalo de ' + variavel, min_value=minimo, max_value=maximo,
                             value=(minimo, maximo), step=1.0)
    mascara &= df[variavel].between(a, b)
else:
    st.sidebar.caption('A variável selecionada só possui um valor.')

st.sidebar.caption('Os filtros afetam os dois dashboards e seus indicadores.')
filtrado = df[mascara]
if filtrado.empty:
    st.warning('Não há acidentes para essa combinação de filtros. Altere a seleção.')
    st.stop()

tab1, tab2 = st.tabs(['📊 Dashboard 1 — Correlação e distribuição', '📈 Dashboard 2 — Indicadores'])

# ----------------------------- Dashboard 1 -----------------------------
with tab1:
    st.subheader('Relação entre variáveis e distribuição dos acidentes')
    e, d = st.columns([1.05, 1], gap='large')
    with e:
        st.markdown('**Matriz de correlação (Pearson)**')
        if len(selecionadas) < 2:
            st.info('Selecione ao menos duas variáveis quantitativas para visualizar a correlação.')
        else:
            matriz = filtrado[selecionadas].corr()
            if matriz.isna().all().all():
                st.warning('Não há observações suficientes para calcular as correlações.')
            else:
                fig = px.imshow(matriz, text_auto='.2f', zmin=-1, zmax=1,
                                color_continuous_scale='RdBu_r', aspect='auto', title='Correlação das contagens')
                fig.update_layout(height=480, coloraxis_colorbar_title='r')
                st.plotly_chart(fig, width='stretch')
                if matriz.isna().any().any():
                    st.caption('Células vazias: alguma variável ficou constante com os filtros atuais.')
    with d:
        st.markdown('**Distribuição da variável selecionada**')
        mostrar_p99 = st.checkbox('Limitar visualização ao percentil 99 (sem alterar indicadores)', value=False)
        distribuicao = filtrado[variavel].dropna()
        if mostrar_p99:
            distribuicao = distribuicao[distribuicao <= distribuicao.quantile(.99)]
        if distribuicao.empty:
            st.info('Sem valores válidos para gerar o histograma.')
        else:
            amostra = distribuicao.sample(min(len(distribuicao), 100000), random_state=42)
            fig = px.histogram(x=amostra, nbins=35, labels={'x': variavel, 'y': 'Quantidade'},
                               title=f'Histograma: {variavel}', color_discrete_sequence=[LARANJA])
            fig.update_layout(height=480, yaxis_title='Ocorrências na amostra exibida')
            st.plotly_chart(fig, width='stretch')
            if len(amostra) < len(distribuicao):
                st.caption('Histograma construído com amostra reprodutível de até 100 mil acidentes.')
    with st.expander('Estatísticas descritivas e interpretação'):
        st.dataframe(filtrado[quant].describe().T.round(2), width='stretch')
        st.caption('Correlação não implica causalidade. Eventos raros e valores extremos foram mantidos nos indicadores.')

# ----------------------------- Dashboard 2 -----------------------------
with tab2:
    st.subheader('Indicadores de frequência e gravidade')
    n = len(filtrado)
    mortes = filtrado['mortos'].sum() if 'mortos' in filtrado else np.nan
    feridos = filtrado['feridos'].sum() if 'feridos' in filtrado else np.nan
    pessoas = filtrado['pessoas'].sum() if 'pessoas' in filtrado else np.nan
    fatais = (filtrado['mortos'].fillna(0) > 0).sum() if 'mortos' in filtrado else np.nan
    kpis = [
        ('Acidentes registrados', formatar(n)),
        ('Pessoas envolvidas', formatar(pessoas)),
        ('Óbitos registrados', formatar(mortes)),
        ('Feridos registrados', formatar(feridos)),
        ('Acidentes com óbito', f'{fatais / n:.1%}'.replace('.', ',') if pd.notna(fatais) else 'N/D'),
    ]
    for coluna, (nome, valor) in zip(st.columns(5), kpis):
        coluna.metric(nome, valor, border=True)
    st.caption('Acidentes com óbito = registros com mortos > 0 ÷ acidentes filtrados. '
               'Não representa risco por quilômetro rodado.')

    # Tabela agregada pequena (UF × ano × classificação × fase do dia): o Altair recebe
    # alguns milhares de linhas em vez de quase 2 milhões.
    grupos = [c for c in ['uf', 'ano', 'classificacao_acidente', 'fase_dia'] if c in filtrado]
    if 'uf' not in grupos or 'mortos' not in filtrado:
        st.info('Colunas UF e mortos são necessárias para os gráficos do Dashboard 2.')
    else:
        agregado = (filtrado.assign(fatal=(filtrado['mortos'].fillna(0) > 0).astype('int32'))
                    .groupby(grupos, observed=True, dropna=False)
                    .agg(acidentes=('fatal', 'size'), fatais=('fatal', 'sum'))
                    .reset_index())
        for c in grupos:
            if c != 'ano':
                agregado[c] = agregado[c].astype('string').fillna('Não informado')

        st.markdown('**Clique em uma UF** para filtrar os outros gráficos (Shift + clique seleciona várias; '
                    'clique duplo limpa).')
        selecao = alt.selection_point(fields=['uf'], on='click', clear='dblclick', empty=True)
        base = alt.Chart(agregado)

        por_uf = (base.mark_bar(cornerRadiusEnd=3)
                  .encode(y=alt.Y('uf:N', sort='-x', title='UF'),
                          x=alt.X('sum(acidentes):Q', title='Acidentes registrados'),
                          color=alt.condition(selecao, alt.value(AZUL), alt.value(CINZA)),
                          tooltip=[alt.Tooltip('uf:N', title='UF'),
                                   alt.Tooltip('sum(acidentes):Q', title='Acidentes', format=',.0f')])
                  .add_params(selecao)
                  .properties(title='Acidentes por UF', width=260, height=640))

        visuais = [por_uf]
        if 'ano' in agregado:
            visuais.append(
                base.transform_filter(selecao).mark_line(point=True, color=AZUL)
                .encode(x=alt.X('ano:O', title='Ano'),
                        y=alt.Y('sum(acidentes):Q', title='Acidentes registrados'),
                        tooltip=[alt.Tooltip('ano:O', title='Ano'),
                                 alt.Tooltip('sum(acidentes):Q', title='Acidentes', format=',.0f')])
                .properties(title='Evolução anual dos acidentes', width=460, height=180))
        if 'classificacao_acidente' in agregado:
            visuais.append(
                base.transform_filter(selecao).mark_bar(color=LARANJA)
                .encode(y=alt.Y('classificacao_acidente:N', sort='-x', title=None),
                        x=alt.X('sum(acidentes):Q', title='Acidentes registrados'),
                        tooltip=[alt.Tooltip('classificacao_acidente:N', title='Classificação'),
                                 alt.Tooltip('sum(acidentes):Q', title='Acidentes', format=',.0f')])
                .properties(title='Acidentes por classificação', width=460, height=150))
        if 'fase_dia' in agregado:
            visuais.append(
                base.transform_filter(selecao)
                .transform_aggregate(acidentes='sum(acidentes)', fatais='sum(fatais)', groupby=['fase_dia'])
                .transform_calculate(pct='datum.fatais / datum.acidentes')
                .mark_bar(color=LARANJA)
                .encode(y=alt.Y('fase_dia:N', sort='-x', title=None),
                        x=alt.X('pct:Q', title='% de acidentes com óbito', axis=alt.Axis(format='%')),
                        tooltip=[alt.Tooltip('fase_dia:N', title='Fase do dia'),
                                 alt.Tooltip('pct:Q', title='% com óbito', format='.1%'),
                                 alt.Tooltip('acidentes:Q', title='Acidentes', format=',.0f')])
                .properties(title='% de acidentes com óbito por fase do dia', width=460, height=150))

        grafico = alt.hconcat(visuais[0], alt.vconcat(*visuais[1:], spacing=28), spacing=40)
        st.altair_chart(grafico.configure_view(stroke=None).configure_title(anchor='start', fontSize=15),
                        width='content')

    st.markdown('**Interpretação**: contagens absolutas descrevem o volume observado, não a probabilidade '
                'individual de acidente. A proporção de acidentes com óbito ajuda a comparar gravidade entre recortes.')

with st.expander('🔎 Conferir registros e qualidade dos dados'):
    st.write(f'Linhas filtradas: {formatar(len(filtrado))} | Variáveis quantitativas disponíveis: {len(quant)}')
    st.dataframe(filtrado.head(500), width='stretch')
