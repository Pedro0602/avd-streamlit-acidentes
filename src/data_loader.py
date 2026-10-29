from pathlib import Path

import pandas as pd
import streamlit as st

# Caminhos relativos à raiz do projeto (funciona local e no Streamlit Community Cloud)
RAIZ = Path(__file__).resolve().parents[1]
PARQUET = RAIZ / "data" / "clean" / "dataset.parquet"
CSV = RAIZ / "data" / "clean" / "dataset.csv"

VARS_QUANT = ["pessoas", "mortos", "feridos_leves", "feridos_graves", "ilesos", "ignorados", "feridos", "veiculos"]
CATEGORIAS = ["uf", "classificacao_acidente", "fase_dia", "condicao_metereologica"]


def arquivo_dados():
    """Parquet primeiro (versionado no Git, ~7 MB); CSV só se o Parquet não existir."""
    return PARQUET if PARQUET.is_file() else CSV


@st.cache_data(show_spinner="Lendo dados tratados...")
def _ler(caminho, modificado):
    if caminho.endswith(".parquet"):
        df = pd.read_parquet(caminho)
    else:
        df = pd.read_csv(caminho, low_memory=False, dtype={c: "category" for c in CATEGORIAS})
    # 'feridos' = feridos_leves + feridos_graves (relação conferida na EDA)
    if "feridos" not in df and {"feridos_leves", "feridos_graves"} <= set(df.columns):
        df["feridos"] = df["feridos_leves"] + df["feridos_graves"]
    for col in VARS_QUANT:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("float32")
    for col in CATEGORIAS:
        if col in df:
            df[col] = df[col].astype("category")
    return df


def load_data():
    """Lê o dataset já tratado (exportado ao final de notebooks/eda-com-downloads.ipynb).

    Fica em cache: o arquivo só é lido de novo se mudar no disco.
    """
    caminho = arquivo_dados()
    if not caminho.is_file():
        raise FileNotFoundError(caminho)
    return _ler(str(caminho), caminho.stat().st_mtime)
