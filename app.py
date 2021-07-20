import streamlit as st

from indicadores import *
from vacinacao import *
from mobilidade import *

########################################################################################################
st.sidebar.title('Menu')
pagina_atual = st.sidebar.selectbox('Selecione o tipo de dados', ['Indicadores', 'Vacinação', 'Mobilidade'])

if pagina_atual == 'Indicadores':
    indicadores()

elif pagina_atual == 'Vacinação':
    vacinacao()

elif pagina_atual == 'Mobilidade':
    mobilidade()