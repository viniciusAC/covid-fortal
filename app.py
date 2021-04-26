import streamlit as st
import numpy as np
import pandas as pd
import datetime

from funcoes_auxiliares.graficos import *

data = pd.read_csv('Base de dados/dados_limpos.csv', sep=';')
data = data.drop(['Unnamed: 0'], axis=1)
data['dataCaso'] = pd.to_datetime(data['dataCaso'])

data2 = pd.read_csv('Base de dados/dados_limpos_full.csv', sep=';')
data2 = data2.drop(['Unnamed: 0'], axis=1)
data2['dataCaso'] = pd.to_datetime(data2['dataCaso'])

bairro_info = pd.read_csv(f'Base de dados/dados_bairros.csv', sep=',')
bairro_info.Bairros	= bairro_info.Bairros.str.upper()
bairro_info = bairro_info.set_index('Bairros')

########################################################################################################
st.sidebar.title('Menu')
pagina_atual = st.sidebar.selectbox('Selecione o tipo de analise', ['Analise geral', 'Analise por bairro', 'Analise por IDH'])

dataAnalise = [datetime.datetime(2020, 1, 1), datetime.date.today()]
dataAnalise[0] = st.sidebar.date_input('Data de inicio', dataAnalise[0], datetime.datetime(2020, 1, 1), datetime.date.today())
dataAnalise[1] = st.sidebar.date_input('Data de termino', dataAnalise[1], dataAnalise[0], datetime.date.today())
dataAnalise = pd.to_datetime(dataAnalise, errors = 'coerce')

dateList = pd.date_range(dataAnalise[0], dataAnalise[1])

filtroDt = (data.dataCaso >= dataAnalise[0]) & (data.dataCaso <= dataAnalise[1])
df = data[filtroDt]
filtroDt = (data2.dataCaso >= dataAnalise[0]) & (data2.dataCaso <= dataAnalise[1])
df2 = data2[filtroDt]

if pagina_atual == 'Analise geral':
    st.markdown('# Analise geral')
    info_basicas(df2)
    grafico_temporal(df2, dateList)
    graficos_idade(df2)
elif pagina_atual == 'Analise por bairro':
    st.markdown('# Analise por bairro')
    
    listBairros = bairro_info.index.tolist()
    values = st.multiselect('Selecione os bairros', listBairros)    

    if len(values) < 1:
        values = listBairros

    filtroBairro = df.bairroCaso.isin(values)
    df_bairros = df[filtroBairro]

    info_basicas(df_bairros)
    grafico_temporal(df_bairros, dateList)
    bairro_table(df_bairros)
    graficos_idade(df_bairros)

elif pagina_atual == 'Analise por IDH':
    st.markdown('# Analise por IDH')
    values = st.slider('Selecione o intervalo do IDH', 0.0, 1.0, (0.100, 0.960))

    filtroIdhMin = bairro_info['IDH em 2010[8]'] >= values[0]
    df_bairrosIdhInfo = bairro_info[filtroIdhMin]
    filtroIdhMax = df_bairrosIdhInfo['IDH em 2010[8]'] <= values[1]
    df_bairrosIdhInfo = df_bairrosIdhInfo[filtroIdhMax]

    filtroBairroIdh = df.bairroCaso.isin(df_bairrosIdhInfo.index.to_list())
    df_bairrosIdh = df[filtroBairroIdh]

    info_basicas(df_bairrosIdh)
    grafico_temporal(df_bairrosIdh, dateList)
    bairro_table(df_bairrosIdh)
    graficos_idade(df_bairrosIdh)