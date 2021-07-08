import numpy as np
import pandas as pd
import streamlit as st

def mob_graphs(dfAtual):
    dfMercado = dfAtual.drop(columns=['retail_and_recreation_percent_change_from_baseline', 'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline'])
    dfParque = dfAtual.drop(columns=['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline'])
    dfResidencias = dfAtual.drop(columns=['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline', 'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline'])
    dfComercio = dfAtual.drop(columns=['grocery_and_pharmacy_percent_change_from_baseline', 'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline'])
    dfPublico =  dfAtual.drop(columns=['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline', 'parks_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline'])
    dfTrabalho = dfAtual.drop(columns=['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline', 'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', 'residential_percent_change_from_baseline'])

    dfMercado.columns = ['date', 'Mercado e Farmácias']
    dfMercado = dfMercado.set_index('date')
    st.markdown('### Mercado e Farmácias')
    st.area_chart(dfMercado)

    dfParque.columns = ['date', 'Parques']
    dfParque = dfParque.set_index('date')
    st.markdown('### Parques')
    st.area_chart(dfParque)

    dfResidencias.columns = ['date', 'Residências']
    dfResidencias = dfResidencias.set_index('date')
    st.markdown('### Residências')
    st.area_chart(dfResidencias)

    dfComercio.columns = ['date', 'Comércio e Lazer']
    dfComercio = dfComercio.set_index('date')
    st.markdown('### Comércio e Lazer')
    st.area_chart(dfComercio)

    dfPublico.columns = ['date', 'Transporte público']
    dfPublico = dfPublico.set_index('date')
    st.markdown('### Transporte público')
    st.area_chart(dfPublico)

    dfTrabalho.columns = ['date', 'Locais de trabalho']
    dfTrabalho = dfTrabalho.set_index('date')
    st.markdown('### Locais de trabalho')
    st.area_chart(dfTrabalho)