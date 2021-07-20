import streamlit as st
import pandas as pd
import numpy as np

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
    filtroObito = (dfAtual.obitoConfirmado == 'Verdadeiro')
    dfObito = dfAtual[filtroObito]

    grouped = dfConfirmado.groupby(['resultadoFinalExame', pd.Grouper(key='dataCaso', freq='W-MON')])['idadeCaso'].mean().reset_index().sort_values('dataCaso')

    quant = list(range(1, len(grouped.idadeCaso.to_list()) + 1 ))
    idade = np.cumsum(grouped.idadeCaso.to_list())
    med = [i/n for i, n in zip(idade, quant)]

    dfConfirmado = {'data': grouped.dataCaso.to_list(), 'Media da idade de casos confirmados': med}
    dfConfirmado = pd.DataFrame(dfConfirmado)
    dfConfirmado = dfConfirmado.set_index('data')

    st.markdown('### Media de idade de casos confirmados')
    st.line_chart(dfConfirmado)

    grouped = dfObito.groupby(['obitoConfirmado', pd.Grouper(key='dataCaso', freq='W-MON')])['idadeCaso'].mean().reset_index().sort_values('dataCaso')

    quant = list(range(1, len(grouped.idadeCaso.to_list()) + 1 ))
    idade = np.cumsum(grouped.idadeCaso.to_list())
    med = [i/n for i, n in zip(idade, quant)]

    dfObito = {'data': grouped.dataCaso.to_list(), 'Media da idade de obitos': med}
    dfObito = pd.DataFrame(dfObito)
    dfObito = dfObito.set_index('data')

    st.markdown('### Media de idade de obitos')
    st.line_chart(dfObito)


def temporal_por_idade(dfAtual):
    filtroConfirmado = (dfAtual.resultadoFinalExame == 'Positivo')
    dfConfirmado = dfAtual[filtroConfirmado]
    dfConfirmado = dfConfirmado[['dataCaso', 'faixaEtaria', 'resultadoFinalExame', 'obitoConfirmado']]
    filtroObito = (dfAtual.obitoConfirmado == 'Verdadeiro')
    dfObito = dfAtual[filtroObito]
    dfObito = dfObito[['dataCaso', 'faixaEtaria', 'obitoConfirmado']]

    grouped = dfConfirmado.groupby(['faixaEtaria', pd.Grouper(key='dataCaso', freq='M')])['resultadoFinalExame'].count().reset_index().sort_values('dataCaso')

    func = {}
    faixa = {'80 ou mais' : '80 ou mais', '65 a 69 anos' : '60 a 69 anos', '55 a 59 anos' : '50 a 59 anos', '70 a 74 anos' : '70 a 79 anos', '75 a 79 anos' : '70 a 79 anos', '60 a 64 anos' : '60 a 69 anos', '50 a 54 anos' : '50 a 59 anos', '40 a 44 anos' : '40 a 49 anos', '45 a 49 anos' : '40 a 49 anos', '35 a 39 anos' : '30 a 39 anos', '30 a 34 anos' : '30 a 39 anos', '25 a 29 anos' : '20 a 29 anos', '20 a 24 anos' : '20 a 29 anos', '00 a 04 anos' : '00 a 09 anos', '15 a 19 anos' : '10 a 19 anos', '05 a 09 anos' : '00 a 09 anos', '10 a 14 anos' : '10 a 19 anos', 'Sem Informacao' : 'i'}
    for i in list(faixa):
        if faixa[i] == 'i':
            continue
        grouped[faixa[i]] = np.where(grouped['faixaEtaria'] == i, grouped['resultadoFinalExame'], 0)
        func[faixa[i]] = 'sum'
    grouped.drop(columns=['faixaEtaria', 'resultadoFinalExame'], inplace=True)

    grouped = grouped.groupby(grouped['dataCaso']).aggregate(func)

    st.markdown('### Casos confirmados por mês, segmentado por idade')
    st.line_chart(grouped)

    grouped2 = dfObito.groupby(['faixaEtaria', pd.Grouper(key='dataCaso', freq='M')])['obitoConfirmado'].count().reset_index().sort_values('dataCaso')

    func2 = {}
    faixa = {'80 ou mais' : '80 ou mais', '65 a 69 anos' : '60 a 69 anos', '55 a 59 anos' : '50 a 59 anos', '70 a 74 anos' : '70 a 79 anos', '75 a 79 anos' : '70 a 79 anos', '60 a 64 anos' : '60 a 69 anos', '50 a 54 anos' : '50 a 59 anos', '40 a 44 anos' : '40 a 49 anos', '45 a 49 anos' : '40 a 49 anos', '35 a 39 anos' : '30 a 39 anos', '30 a 34 anos' : '30 a 39 anos', '25 a 29 anos' : '20 a 29 anos', '20 a 24 anos' : '20 a 29 anos', '00 a 04 anos' : '00 a 09 anos', '15 a 19 anos' : '10 a 19 anos', '05 a 09 anos' : '00 a 09 anos', '10 a 14 anos' : '10 a 19 anos', 'Sem Informacao' : 'i'}
    for i in list(faixa):
        if faixa[i] == 'i':
            continue
        grouped2[faixa[i]] = np.where(grouped2['faixaEtaria'] == i, grouped2['obitoConfirmado'], 0)
        func2[faixa[i]] = 'sum'
    grouped2.drop(columns=['faixaEtaria', 'obitoConfirmado'], inplace=True)

    grouped2 = grouped2.groupby(grouped2['dataCaso']).aggregate(func2)

    st.markdown('### Obitos por mês, segmentado por idade')
    st.line_chart(grouped2)

    grouped2.rename(columns={'80 ou mais': '80 ou mais O', '60 a 69 anos' : '60 a 69 anos O', '50 a 59 anos' : '50 a 59 anos O', '70 a 79 anos' : '70 a 79 anos O', '40 a 49 anos' : '40 a 49 anos O', '30 a 39 anos' : '30 a 39 anos O', '20 a 29 anos' : '20 a 29 anos O', '00 a 09 anos' : '00 a 09 anos O', '10 a 19 anos' : '10 a 19 anos O'}, inplace=True)

    result = pd.concat([grouped2, grouped], axis=1)
    result.fillna(0, inplace=True)
    for i in list(func):
        result[i] = result[i+' O'] * 100 / result[i]
        result.drop(columns=[i + ' O'], inplace=True)
    result.fillna(0, inplace=True)
    
    st.markdown('### Letalidade por mês, segmentado por idade (em porcentagem)')
    st.line_chart(result)

    
