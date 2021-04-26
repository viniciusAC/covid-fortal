import streamlit as st
import numpy as np
import pandas as pd
import datetime

def grafico_temporal(dfAtual, date_list):
    infectadosPorDia = []
    suspeitosPorDia = []
    obtosPorDia = []
    for i in date_list:
        filtroDia = dfAtual.dataCaso == i
        dfTempData = dfAtual[filtroDia]
        infectadosPorDia.append(dfTempData[dfTempData.resultadoFinalExame == 'Positivo'].shape[0])
        suspeitosPorDia.append(-dfTempData[dfTempData.resultadoFinalExame == 'Suspeito'].shape[0])
        obtosPorDia.append(dfTempData[dfTempData.obitoConfirmado == 'Verdadeiro'].shape[0])

    GrafDiaInfo = np.array([date_list, infectadosPorDia, suspeitosPorDia])
    dfGrafDia = pd.DataFrame(GrafDiaInfo.T, columns=["data", "casos confirmados", "casos suspeitos"])
    dfGrafDia = dfGrafDia.set_index('data')

    GrafObitosDiaInfo = np.array([date_list, obtosPorDia])
    dfObitoGrafDia = pd.DataFrame(GrafObitosDiaInfo.T, columns=["data", "obitos"])
    dfObitoGrafDia = dfObitoGrafDia.set_index('data')

    st.title(date_list[0])

    st.markdown('### Mostragem dos casos')
    st.bar_chart(dfGrafDia)

    st.markdown('### Mostragem dos obitos')
    st.bar_chart(dfObitoGrafDia)

def bairro_table(dfAtual):
    dados = []
    for i in dfAtual.bairroCaso.value_counts().index:
        filtroBairro = dfAtual.bairroCaso == i
        dfTemp = dfAtual[filtroBairro]
        dados.append([i, 
                    dfTemp[dfTemp.resultadoFinalExame == 'Positivo'].shape[0],
                    dfTemp[dfTemp.resultadoFinalExame == 'Suspeito'].shape[0],
                    dfTemp[dfTemp.obitoConfirmado == 'Verdadeiro'].shape[0]])
    
    dfGrafBairro = pd.DataFrame(dados, columns=["Bairro", "casos confirmados", "casos suspeitos", "obitos"])

    st.markdown('### Dados dos bairros')
    st.dataframe(dfGrafBairro)

def graficos_idade(dfAtual):
    dadosPositivos = []
    dadosObito = []
    for i in dfAtual.faixaEtaria.value_counts().index:
        filtroFaixaEtaria = dfAtual.faixaEtaria == i
        dfTemp = dfAtual[filtroFaixaEtaria]

        filtro = ((dfTemp.resultadoFinalExame == 'Positivo') )
        dfPositivo = dfTemp[filtro]

        filtro = ((dfTemp.obitoConfirmado == 'Verdadeiro') )
        dfObito = dfTemp[filtro]

        dadosPositivos.append([i, 
                        dfPositivo[dfPositivo.sexoCaso == 'FEMININO'].shape[0],
                        -dfPositivo[dfPositivo.sexoCaso == 'MASCULINO'].shape[0]])
        
        dadosObito.append([i, 
                        dfObito[dfObito.sexoCaso == 'FEMININO'].shape[0],
                        -dfObito[dfObito.sexoCaso == 'MASCULINO'].shape[0]])
    
    dfGrafPositivo = pd.DataFrame(dadosPositivos, columns=["faixa Etaria", "feminino", "masculino"])
    dfGrafPositivo = dfGrafPositivo.set_index("faixa Etaria")

    dfGrafObito = pd.DataFrame(dadosObito, columns=["faixa Etaria", "feminino", "masculino"])
    dfGrafObito = dfGrafObito.set_index("faixa Etaria")

    st.markdown('### Casos por faixa etaria e genero')
    st.bar_chart(dfGrafPositivo)

    st.markdown('### Obitos por faixa etaria e genero')
    st.bar_chart(dfGrafObito)

def info_basicas(dfAtual):
    confirmados = dfAtual[dfAtual.resultadoFinalExame == 'Positivo'].shape[0]
    obitos = dfAtual[dfAtual.obitoConfirmado == 'Verdadeiro'].shape[0]
    infos = [[dfAtual.shape[0], confirmados, obitos, (obitos/confirmados)*100], [dfAtual.shape[0], confirmados, obitos, (obitos/confirmados)*100], [dfAtual.shape[0], confirmados, obitos, (obitos/confirmados)*100], [dfAtual.shape[0], confirmados, obitos, (obitos/confirmados)*100]]
    dfInfo = pd.DataFrame(infos, columns=["Casos noticados", "Casos confirmados", "Obitos", "Letalidade"])

    st.table(dfInfo.head(1))