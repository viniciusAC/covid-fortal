import json
import plotly.express as px
import datetime
import streamlit as st
import pandas as pd

def mapa(counties, dfAtual, coluna):
    try:
        fig = px.choropleth_mapbox(dfAtual, geojson=counties, locations='Bairros', color=coluna,
                                    color_continuous_scale=[(0, "white"), (0.5, "yellow"), (1, "red")],
                                    range_color=(0, dfAtual[f'{coluna}'].max()),
                                    mapbox_style="carto-positron",
                                    zoom=10.5, center = {"lat": -3.7789976, "lon": -38.5401627},
                                    opacity=0.8
                                    )
    except:
        st.text('Nenhum caso notificado')
        return
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

def conjunto_mapa(dfAtual, bairro_info):
    f = open('Base_de_dados/FortalezaBairros.geojson',)
    counties = json.load(f)

    for x in counties['features']:
        x['id'] = x['properties']['NOME']
        if x['id'] == 'ALTO DA BALANCA':
            x['id'] = 'ALTO DA BALANÇA'
        elif x['id'] == 'COACU':
            x['id'] = 'COAÇU'
        elif x['id'] == 'CONJUNTO ESPERANCA':
            x['id'] = 'CONJUNTO ESPERANÇA'

    dadosObito = []
    dadosObitoPercent = []
    dadosConfirmado = []
    dadosConfirmadoPercent = []
    indiceDeTransmicao = []
    for i in bairro_info.index.to_list():
        if i == 'Indeterminado':
            continue
        filtroBairro = dfAtual.bairroCaso == i
        dfTemp = dfAtual[filtroBairro]
        dadosObito.append([i, dfTemp[dfTemp.obitoConfirmado == 'Verdadeiro'].shape[0]])
        dadosObitoPercent.append([i, 100 * dfTemp[dfTemp.obitoConfirmado == 'Verdadeiro'].shape[0]/bairro_info.loc[i][1]])
        dadosConfirmado.append([i, dfTemp[dfTemp.resultadoFinalExame == 'Positivo'].shape[0]])
        dadosConfirmadoPercent.append([i, 100 * dfTemp[dfTemp.resultadoFinalExame == 'Positivo'].shape[0]/bairro_info.loc[i][1]])

        if dfTemp['dataCaso'].empty:
            continue

        filtroDt = (dfTemp.dataCaso >= dfTemp['dataCaso'].max() - datetime.timedelta(14)) & (dfTemp.dataCaso <= dfTemp['dataCaso'].max() - datetime.timedelta(7))
        dfDiasAtras = dfTemp[filtroDt]
        positivados = dfDiasAtras[dfDiasAtras.resultadoFinalExame == 'Positivo'].shape[0]

        filtroDt = (dfTemp.dataCaso >= dfTemp['dataCaso'].max() - datetime.timedelta(21)) & (dfTemp.dataCaso <= dfTemp['dataCaso'].max() - datetime.timedelta(14))
        dfDiasAtras = dfTemp[filtroDt]
        if dfDiasAtras[dfDiasAtras.resultadoFinalExame == 'Positivo'].shape[0] == 0:
            continue
        else:
            indiceDeTransmicao.append([i, positivados/dfDiasAtras[dfDiasAtras.resultadoFinalExame == 'Positivo'].shape[0]])

    st.markdown('### Mapa com informações dos bairros')
    tipoMapa = st.selectbox('Selecione a informação', ['Taxa de contaminação',
                                                                'Total de casos confirmados', 
                                                                'Total de obitos', 
                                                                '% Caso confirmado por População', 
                                                                '% Obitos por População'])

    if tipoMapa == 'Taxa de contaminação':
        dfTaxaCont = pd.DataFrame(indiceDeTransmicao, columns=["Bairros", "Taxa de contaminação"])
        mapa(counties, dfTaxaCont, "Taxa de contaminação")
    elif tipoMapa == 'Total de casos confirmados':
        dfConfirmado = pd.DataFrame(dadosConfirmado, columns=["Bairros", "Casos positivos"])
        mapa(counties, dfConfirmado, "Casos positivos")
    elif tipoMapa == 'Total de obitos':
        dfObito = pd.DataFrame(dadosObito, columns=["Bairros", "Obitos"])
        mapa(counties, dfObito, "Obitos")
    elif tipoMapa == '% Caso confirmado por População':
        dfConfirmadoCent = pd.DataFrame(dadosConfirmadoPercent, columns=["Bairros", "% Caso confirmado por População"])
        mapa(counties, dfConfirmadoCent, "% Caso confirmado por População")
    elif tipoMapa == '% Obitos por População':
        dfObitoCent = pd.DataFrame(dadosObitoPercent, columns=["Bairros", "% Obitos por População"])
        mapa(counties, dfObitoCent, "% Obitos por População")
