"""Baixa a base Kaggle usada na EDA e exporta o dataset tratado para o Streamlit.

Saída: data/clean/dataset.csv (só as colunas usadas no app, com a data reduzida ao ano
para o arquivo caber no GitHub e na memória do Streamlit Community Cloud).
"""
from pathlib import Path
import pandas as pd
import kagglehub

ROOT = Path(__file__).resolve().parents[1]
saida = ROOT / 'data' / 'clean' / 'dataset.csv'
saida.parent.mkdir(parents=True, exist_ok=True)

pasta = Path(kagglehub.dataset_download('marcosfnlr/acidentes-em-rodovias-federais-20072020'))
arquivos = list(pasta.rglob('acidentes2007-2020.csv')) or list(pasta.rglob('*.csv'))
if not arquivos:
    raise FileNotFoundError('Nenhum CSV encontrado no download do Kaggle.')
arquivo = arquivos[0]
print('Origem:', arquivo)

QUANT = ['pessoas', 'mortos', 'feridos_leves', 'feridos_graves', 'ilesos', 'ignorados', 'feridos', 'veiculos']
CATEG = ['uf', 'classificacao_acidente', 'fase_dia', 'condicao_metereologica']
cabecalho = pd.read_csv(arquivo, nrows=0).columns.tolist()
# Nesta versão do Kaggle a data do acidente está no fim de id_unico (ex.: '102007-06-11').
existentes = [c for c in ['id_unico'] + CATEG + QUANT if c in cabecalho]
if not any(c in existentes for c in ('pessoas', 'mortos', 'feridos', 'veiculos')):
    raise ValueError('Dataset sem colunas quantitativas esperadas. Confira o arquivo Kaggle.')

partes = []
# A base original usa o texto '(null)' para campos não preenchidos: vira valor ausente.
for lote in pd.read_csv(arquivo, usecols=existentes, chunksize=200000, low_memory=False,
                        na_values=['(null)']):
    if 'id_unico' in lote:
        data = lote['id_unico'].astype('string').str[-10:]
        lote['ano'] = pd.to_datetime(data, errors='coerce', format='%Y-%m-%d').dt.year.astype('Int16')
        lote = lote.drop(columns='id_unico')
    for c in QUANT:
        if c in lote:
            lote[c] = pd.to_numeric(lote[c], errors='coerce').astype('Int32')
    for c in CATEG:
        if c in lote:
            lote[c] = lote[c].astype('string').str.strip()
    partes.append(lote)

df = pd.concat(partes, ignore_index=True)
# 'feridos' é sempre feridos_leves + feridos_graves (conferido na EDA): o app recalcula,
# e tirar a coluna mantém o CSV abaixo do limite de 100 MB por arquivo do GitHub.
if {'feridos', 'feridos_leves', 'feridos_graves'} <= set(df.columns):
    assert (df['feridos'] == df['feridos_leves'] + df['feridos_graves']).all()
    df = df.drop(columns='feridos')
df = df[[c for c in ['ano'] + CATEG + QUANT if c in df.columns]]
df.to_csv(saida, index=False)
tamanho = saida.stat().st_size / 1024 ** 2
print(f'Salvo em {saida}: {len(df):,} registros / {len(df.columns)} colunas / {tamanho:.1f} MB')

# Cópia em Parquet com tipos compactos: o app lê esta versão primeiro (menos memória no deploy).
compacto = df.copy()
for c in CATEG:
    if c in compacto:
        compacto[c] = compacto[c].astype('category')
for c in compacto.columns.difference(CATEG):
    compacto[c] = pd.to_numeric(compacto[c], downcast='integer')
parquet = saida.with_suffix('.parquet')
compacto.to_parquet(parquet, index=False)
print(f'Salvo em {parquet}: {parquet.stat().st_size / 1024 ** 2:.1f} MB')
