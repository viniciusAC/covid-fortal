import streamlit as st
import pandas as pd
import datetime

from funcoes_auxiliares.mobility_graphs import *

def mobilidade():
    mob = pd.read_csv('Base_de_dados/mobilidade.csv', sep=';')
    mob = mob.drop(['Unnamed: 0'], axis=1)
    mob['date'] = pd.to_datetime(mob['date'])

    dataAnalise = [datetime.datetime(2020, 3, 1), mob['date'].max()]
    dataAnalise[0] = st.sidebar.date_input('Data de inicio', dataAnalise[0], datetime.datetime(2020, 3, 1), mob['date'].max())
    dataAnalise[1] = st.sidebar.date_input('Data de termino', dataAnalise[1], dataAnalise[0], mob['date'].max())
    dataAnalise = pd.to_datetime(dataAnalise, errors = 'coerce')
    
    filtroDt = (mob.date >= dataAnalise[0]) & (mob.date <= dataAnalise[1])
    df4 = mob[filtroDt]

    st.markdown('# Analise de Mobilidade')
    mob_graphs(df4)