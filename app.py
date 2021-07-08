import streamlit as st
import pandas as pd
import datetime

from funcoes_auxiliares.graficos import *
from funcoes_auxiliares.VacGraphs import *
from funcoes_auxiliares.Maps import *
from funcoes_auxiliares.mobility_graphs import *

data = pd.read_csv('Base_de_dados/dados_limpos.csv', sep=';')
data = data.drop(['Unnamed: 0'], axis=1)
data['dataCaso'] = pd.to_datetime(data['dataCaso'])
# data['dataCaso'] = data['dataCaso'].dt.date

data.sort_values(by=['identificadorCaso', 'resultadoFinalExame'], inplace=True)  
# data.drop_duplicates(subset='identificadorCaso', keep='last', inplace=True)
# data = data.drop(columns=['identificadorCaso'])

bairro_info = pd.read_csv(f'Base_de_dados/dados_bairros.csv', sep=',')
bairro_info.Bairros	= bairro_info.Bairros.str.upper()
bairro_info = bairro_info.set_index('Bairros')

vacinados = pd.read_csv('Base_de_dados/vacinados.csv', sep=';')
vacinados = vacinados.drop(['Unnamed: 0'], axis=1)
vacinados['vacina_dataaplicacao'] = pd.to_datetime(vacinados['vacina_dataaplicacao'])
vacinados['vacina_dataaplicacao'] = vacinados['vacina_dataaplicacao'].dt.date

mob = pd.read_csv('Base_de_dados/mobilidade.csv', sep=';')
mob = mob.drop(['Unnamed: 0'], axis=1)
mob['date'] = pd.to_datetime(mob['date'])

########################################################################################################
st.sidebar.title('Menu')
pagina_atual = st.sidebar.selectbox('Selecione o tipo de analise', ['Analise geral', 'Analise segmentada', 'Analise por bairro', 
                                                                    'Analise por IDH', 'Vacinação geral', 'Vacinação por grupos', 
                                                                    'Vacinação por idade', 'Mobilidade'])

dataAnalise = [datetime.datetime(2020, 1, 1), data['dataCaso'].max()]
dataAnalise[0] = st.sidebar.date_input('Data de inicio', dataAnalise[0], datetime.datetime(2020, 1, 1), data['dataCaso'].max())
dataAnalise[1] = st.sidebar.date_input('Data de termino', dataAnalise[1], dataAnalise[0], data['dataCaso'].max())
dataAnalise = pd.to_datetime(dataAnalise, errors = 'coerce')

filtroDt = (data.dataCaso >= dataAnalise[0]) & (data.dataCaso <= dataAnalise[1])
df1 = data[filtroDt]
filtroDt = (vacinados.vacina_dataaplicacao >= dataAnalise[0]) & (vacinados.vacina_dataaplicacao <= dataAnalise[1])
df3 = vacinados[filtroDt]
filtroDt = (mob.date >= dataAnalise[0]) & (mob.date <= dataAnalise[1])
df4 = mob[filtroDt]

if pagina_atual == 'Analise geral':
    st.markdown('# Analise geral')
    info_basicas(df1)
    grafico_temporal(df1)
    graficos_idade(df1)
    Idade_media(df1)
    conjunto_mapa(df1, bairro_info)
    
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
    conjunto_mapa(df_bairros, bairro_info)

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
    idhXgraph(df_bairrosIdh, bairro_info)
    graficos_idade(df_bairrosIdh)
    conjunto_mapa(df_bairrosIdh, bairro_info)

elif pagina_atual == 'Vacinação geral':
    st.markdown('# Vacinação em Fortaleza')
    vacinas_dias(df3)
    tipo_vac(df3)
    vacinacao_grupo(df3)

elif pagina_atual == 'Analise segmentada':
    st.markdown('# Analise segmentada')
    seg_atual = st.selectbox('Selecione o segmento de analise', ['Idade', 'Profissional da saude', 'Profissão'])

    if seg_atual == 'Idade':
        st.markdown('# Analise por idade')
        values = st.slider('Selecione o intervalo de idade', 0, 110, (0, 110))

        filtroIdadeMin = df1['idadeCaso'] >= values[0]
        df_idade = df1[filtroIdadeMin]
        filtroIdadeMax = df_idade['idadeCaso'] <= values[1]
        df_idade = df_idade[filtroIdadeMax]

        info_basicas(df_idade)
        grafico_temporal(df_idade)
        graficos_idade(df_idade)
        conjunto_mapa(df_idade, bairro_info)

    elif seg_atual == 'Profissional da saude':
        st.markdown('# Analise de profissionais da saude')

        filtroSaude = df1['profissionalSaudeEsus'] == True
        df_PSaude = df1[filtroSaude]

        info_basicas(df_PSaude)
        grafico_temporal(df_PSaude)
        graficos_idade(df_PSaude)
        conjunto_mapa(df_PSaude, bairro_info)

    elif seg_atual == 'Profissão':
        listpProf = df1.profissoes.value_counts().index.to_list()
        values = st.multiselect('Selecione as profissões', listpProf)    

        if len(values) < 1:
            values = listpProf

        filProf = df1.profissoes.isin(values)
        df_profissao = df1[filProf]

        info_basicas(df_profissao)
        grafico_temporal(df_profissao)
        graficos_idade(df_profissao)
        conjunto_mapa(df_profissao, bairro_info)

elif pagina_atual == 'Vacinação por grupos':
    listGrupo = df3.grupoVacinacao.value_counts().index.to_list()
    values = st.multiselect('Selecione o grupo', listGrupo)    

    if len(values) < 1:
        values = listGrupo

    filGrupo = df3.grupoVacinacao.isin(values)
    df_grupo_vacinacao = df3[filGrupo]

    vacinas_dias(df_grupo_vacinacao)
    tipo_vac(df_grupo_vacinacao)
    vacinacao_grupo(df_grupo_vacinacao)

elif pagina_atual == 'Vacinação por idade':
    st.markdown('# Analise por idade')
    values = st.slider('Selecione o intervalo de idade', 0, 110, (0, 110))

    filtroIdadeMin = df3['paciente_idade'] >= values[0]
    df_idade = df3[filtroIdadeMin]
    filtroIdadeMax = df_idade['paciente_idade'] <= values[1]
    df_idade = df_idade[filtroIdadeMax]

    vacinas_dias(df_idade)
    tipo_vac(df_idade)
    vacinacao_grupo(df_idade)

elif pagina_atual == 'Mobilidade':
    st.markdown('# Analise de Mobilidade')

    mob_graphs(df4)