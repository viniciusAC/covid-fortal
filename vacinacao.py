import streamlit as st
import pandas as pd 
import datetime

from funcoes_auxiliares.VacGraphs import *

def vacinacao():
    vacinados = pd.read_csv('Base_de_dados/vacinados.csv', sep=';')
    vacinados = vacinados.drop(['Unnamed: 0'], axis=1)
    vacinados['vacina_dataaplicacao'] = pd.to_datetime(vacinados['vacina_dataaplicacao'])
    vacinados['vacina_dataaplicacao'] = vacinados['vacina_dataaplicacao'].dt.date

    analise = st.sidebar.selectbox('Selecione o tipo de analise', ['Vacinação geral', 'Vacinação por grupos', 'Vacinação por idade'])

    dataAnalise = [datetime.datetime(2020, 3, 1), vacinados['vacina_dataaplicacao'].max()]
    dataAnalise[0] = st.sidebar.date_input('Data de inicio', dataAnalise[0], datetime.datetime(2020, 3, 1), vacinados['vacina_dataaplicacao'].max())
    dataAnalise[1] = st.sidebar.date_input('Data de termino', dataAnalise[1], dataAnalise[0], vacinados['vacina_dataaplicacao'].max())
    dataAnalise = pd.to_datetime(dataAnalise, errors = 'coerce')

    filtroDt = (vacinados.vacina_dataaplicacao >= dataAnalise[0]) & (vacinados.vacina_dataaplicacao <= dataAnalise[1])
    df3 = vacinados[filtroDt]

    if analise == 'Vacinação geral':
        st.markdown('# Vacinação em Fortaleza')
        vacinas_dias(df3)
        tipo_vac(df3)
        vacinacao_grupo(df3)

    elif analise == 'Vacinação por grupos':
        listGrupo = df3.grupoVacinacao.value_counts().index.to_list()
        values = st.multiselect('Selecione o grupo', listGrupo)    

        if len(values) < 1:
            values = listGrupo

        filGrupo = df3.grupoVacinacao.isin(values)
        df_grupo_vacinacao = df3[filGrupo]

        vacinas_dias(df_grupo_vacinacao)
        tipo_vac(df_grupo_vacinacao)
        vacinacao_grupo(df_grupo_vacinacao)

    elif analise == 'Vacinação por idade':
        st.markdown('# Analise por idade')
        values = st.slider('Selecione o intervalo de idade', 0, 110, (0, 110))

        filtroIdadeMin = df3['paciente_idade'] >= values[0]
        df_idade = df3[filtroIdadeMin]
        filtroIdadeMax = df_idade['paciente_idade'] <= values[1]
        df_idade = df_idade[filtroIdadeMax]

        vacinas_dias(df_idade)
        tipo_vac(df_idade)
        vacinacao_grupo(df_idade)