import streamlit as st
import numpy as np
import pandas as pd
import datetime

from funcoes_auxiliares.graficos import *

data = pd.read_csv('Base de dados/dados_limpos.csv', sep=';')
data = data.drop(['Unnamed: 0'], axis=1)
data['dataCaso'] = pd.to_datetime(data['dataCaso'])
data['dataCaso'] = data['dataCaso'].dt.date

# data.sort_values(by=['resultadoFinalExame'], inplace=True)  
# data.drop_duplicates(subset='identificadorCaso', keep='last', inplace=True)
# data = data.drop(columns=['identificadorCaso'])

bairro_info = pd.read_csv(f'Base de dados/dados_bairros.csv', sep=',')
bairro_info.Bairros	= bairro_info.Bairros.str.upper()
bairro_info = bairro_info.set_index('Bairros')

vacinados = pd.read_csv('Base de dados/vacinados.csv', sep=';')
vacinados = vacinados.drop(['Unnamed: 0'], axis=1)
vacinados['data_vacinação'] = pd.to_datetime(vacinados['data_vacinação'])
vacinados['data_vacinação'] = vacinados['data_vacinação'].dt.date

########################################################################################################
st.sidebar.title('Menu')
pagina_atual = st.sidebar.selectbox('Selecione o tipo de analise', ['Analise geral', 'Analise por bairro', 'Analise por IDH', 'Vacinação'])

dataAnalise = [datetime.datetime(2021, 3, 1), datetime.date.today()]
dataAnalise[0] = st.sidebar.date_input('Data de inicio', dataAnalise[0], datetime.datetime(2020, 1, 1), datetime.date.today())
dataAnalise[1] = st.sidebar.date_input('Data de termino', dataAnalise[1], dataAnalise[0], datetime.date.today())
dataAnalise = pd.to_datetime(dataAnalise, errors = 'coerce')

filtroDt = (data.dataCaso >= dataAnalise[0]) & (data.dataCaso <= dataAnalise[1])
df1 = data[filtroDt]
filtroDt = (vacinados.data_vacinação >= dataAnalise[0]) & (vacinados.data_vacinação <= dataAnalise[1])
df3 = vacinados[filtroDt]

if pagina_atual == 'Analise geral':
    st.markdown('# Analise geral')
    info_basicas(df1)
    grafico_temporal(df1)
    graficos_idade(df1)
    
elif pagina_atual == 'Analise por bairro':
    st.markdown('# Analise por bairro')
    
    listBairros = bairro_info.index.tolist()
    values = st.multiselect('Selecione os bairros', listBairros)    

    if len(values) < 1:
        values = listBairros

    filtroBairro = df1.bairroCaso.isin(values)
    df_bairros = df1[filtroBairro]

    info_basicas(df_bairros)
    grafico_temporal(df_bairros)
    bairro_table(df_bairros)
    graficos_idade(df_bairros)

elif pagina_atual == 'Analise por IDH':
    st.markdown('# Analise por IDH')
    values = st.slider('Selecione o intervalo do IDH', 0.0, 1.0, (0.0, 1.0))

    filtroIdhMin = bairro_info['IDH em 2010[8]'] >= values[0]
    df_bairrosIdhInfo = bairro_info[filtroIdhMin]
    filtroIdhMax = df_bairrosIdhInfo['IDH em 2010[8]'] <= values[1]
    df_bairrosIdhInfo = df_bairrosIdhInfo[filtroIdhMax]

    filtroBairroIdh = df1.bairroCaso.isin(df_bairrosIdhInfo.index.to_list())
    df_bairrosIdh = df1[filtroBairroIdh]

    info_basicas(df_bairrosIdh)
    grafico_temporal(df_bairrosIdh)
    bairro_idh_table(df_bairrosIdh, bairro_info)
    idhXobitos(df_bairrosIdh, bairro_info)
    idhXconfirmdo(df_bairrosIdh, bairro_info)
    graficos_idade(df_bairrosIdh)

elif pagina_atual == 'Vacinação':
    st.markdown('# Vacinação em Fortaleza')
    vacinas_dias(df3)
    vacinacao_grupo(df3)