import streamlit as st
import pandas as pd

def grafico_temporal(dfAtual):
    infectadosPorDia = []
    #suspeitosPorDia = []
    obtosPorDia = []
    date_list = []
    grouped = dfAtual.groupby(['dataCaso'])
    for name, group in grouped:
        date_list.append(name)
        infectadosPorDia.append(group[group.resultadoFinalExame == 'Positivo'].shape[0])
        obtosPorDia.append(group[group.obitoConfirmado == 'Verdadeiro'].shape[0])

    GrafDiaInfo = {'data': date_list, 'casos confirmados': infectadosPorDia}
    dfGrafDia = pd.DataFrame(GrafDiaInfo)
    dfGrafDia = dfGrafDia.set_index('data')

    GrafObitosDiaInfo = {'data': date_list, 'obitos': obtosPorDia}
    dfObitoGrafDia = pd.DataFrame(GrafObitosDiaInfo)
    dfObitoGrafDia = dfObitoGrafDia.set_index('data')

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
                    dfTemp[dfTemp.resultadoFinalExame == 'Caso suspeito'].shape[0],
                    dfTemp[dfTemp.obitoConfirmado == 'Verdadeiro'].shape[0]])
    
    dfGrafBairro = pd.DataFrame(dados, columns=["Bairro", "casos confirmados", "casos suspeitos", "obitos"])

    st.markdown('### Dados dos bairros')
    st.dataframe(dfGrafBairro)


def bairro_idh_table(dfAtual, bairro_info):
    dados = []
    for i in dfAtual.bairroCaso.value_counts().index:
        filtroBairro = dfAtual.bairroCaso == i
        dfTemp = dfAtual[filtroBairro]
        dados.append([bairro_info.loc[i][0], i, 
                    dfTemp[dfTemp.resultadoFinalExame == 'Positivo'].shape[0],
                    dfTemp[dfTemp.resultadoFinalExame == 'Caso suspeito'].shape[0],
                    dfTemp[dfTemp.obitoConfirmado == 'Verdadeiro'].shape[0]])
    
    dfGrafBairro = pd.DataFrame(dados, columns=["IDH", "bairro", "casos confirmados", "casos suspeitos", "obitos"])
    dfGrafBairro.sort_values(by=['IDH'], inplace=True, ascending=False, ignore_index=True)

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
                        dfPositivo[dfPositivo.sexoCaso == 'MASCULINO'].shape[0]])
        
        dadosObito.append([i, 
                        dfObito[dfObito.sexoCaso == 'FEMININO'].shape[0],
                        dfObito[dfObito.sexoCaso == 'MASCULINO'].shape[0]])
    
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
    dfInfo = pd.DataFrame(infos, columns=["Casos notificados", "Casos confirmados", "Obitos", "Letalidade"])

    st.table(dfInfo.head(1))


def idhXgraph(dfAtual, bairro_info):
    dadosObito = []
    dadosConfirmado = []
    for i in dfAtual.bairroCaso.value_counts().index:
        filtroBairro = dfAtual.bairroCaso == i
        dfTemp = dfAtual[filtroBairro]
        dadosObito.append([bairro_info.loc[i][0], 
                    dfTemp[dfTemp.obitoConfirmado == 'Verdadeiro'].shape[0]])
        dadosConfirmado.append([bairro_info.loc[i][0], 
                    dfTemp[dfTemp.resultadoFinalExame == 'Positivo'].shape[0]])
    
    dfIdhConfirmado = pd.DataFrame(dadosConfirmado, columns=["IDH", "Casos positivos"])

    st.markdown('### IDH X Casos positivos')
    st.vega_lite_chart(dfIdhConfirmado, {
        "height": 300,
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'IDH', 'type': 'quantitative'},
            'y': {'field': 'Casos positivos', 'type': 'quantitative'}
        },
    }, use_container_width = True)

    dfIdhObito = pd.DataFrame(dadosObito, columns=["IDH", "Obitos"])

    st.markdown('### IDH X Obitos')
    st.vega_lite_chart(dfIdhObito, {
        "height": 300,
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'IDH', 'type': 'quantitative'},
            'y': {'field': 'Obitos', 'type': 'quantitative'}
        },
    }, use_container_width = True)


def Idade_media(dfAtual):
    filtroConfirmado = (dfAtual.resultadoFinalExame == 'Positivo')
    dfConfirmado = dfAtual[filtroConfirmado]
    filtroObito = (dfConfirmado.obitoConfirmado == 'Verdadeiro')
    dfObito = dfConfirmado[filtroObito]

    grouped = dfConfirmado.groupby(['resultadoFinalExame', pd.Grouper(key='dataCaso', freq='W-MON')])['idadeCaso'].mean().reset_index().sort_values('dataCaso')

    dfConfirmado = {'data': grouped.dataCaso.to_list(), 'Media da idade de casos confirmados': grouped.idadeCaso.to_list()}
    dfConfirmado = pd.DataFrame(dfConfirmado)
    dfConfirmado = dfConfirmado.set_index('data')

    st.markdown('### Media de idade de casos confirmados')
    st.line_chart(dfConfirmado)

    grouped = dfObito.groupby(['obitoConfirmado', pd.Grouper(key='dataCaso', freq='W-MON')])['idadeCaso'].mean().reset_index().sort_values('dataCaso')

    dfObito = {'data': grouped.dataCaso.to_list(), 'Media da idade de obitos': grouped.idadeCaso.to_list()}
    dfObito = pd.DataFrame(dfObito)
    dfObito = dfObito.set_index('data')

    st.markdown('### Media de idade de obitos')
    st.line_chart(dfObito)
    