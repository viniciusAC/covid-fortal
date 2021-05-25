import streamlit as st
import numpy as np
import pandas as pd
import datetime


def grafico_temporal(dfAtual):
    infectadosPorDia = []
    #suspeitosPorDia = []
    obtosPorDia = []
    date_list = []
    grouped = dfAtual.groupby(['dataCaso'])
    for name, group in grouped:
        date_list.append(name)
        infectadosPorDia.append(group[group.resultadoFinalExame == 'Positivo'].shape[0])
        #suspeitosPorDia.append(-group[group.resultadoFinalExame == 'Caso suspeito'].shape[0])
        obtosPorDia.append(group[group.obitoConfirmado == 'Verdadeiro'].shape[0])

    #GrafDiaInfo = {'data': date_list, 'casos confirmados': infectadosPorDia, 'casos caso suspeito': suspeitosPorDia}
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


def idhXobitos(dfAtual, bairro_info):
    dados = []
    for i in dfAtual.bairroCaso.value_counts().index:
        filtroBairro = dfAtual.bairroCaso == i
        dfTemp = dfAtual[filtroBairro]
        dados.append([bairro_info.loc[i][0], 
                    dfTemp[dfTemp.obitoConfirmado == 'Verdadeiro'].shape[0]])
    
    dfIdhObito = pd.DataFrame(dados, columns=["IDH", "obitos"])

    st.markdown('### IDH X Obitos')
    st.vega_lite_chart(dfIdhObito, {
        "height": 300,
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'IDH', 'type': 'quantitative'},
            'y': {'field': 'obitos', 'type': 'quantitative'}
        },
    }, use_container_width = True)


def idhXconfirmdo(dfAtual, bairro_info):
    dados = []
    for i in dfAtual.bairroCaso.value_counts().index:
        filtroBairro = dfAtual.bairroCaso == i
        dfTemp = dfAtual[filtroBairro]
        dados.append([bairro_info.loc[i][0], 
                    dfTemp[dfTemp.resultadoFinalExame == 'Positivo'].shape[0]])
    
    dfIdhObito = pd.DataFrame(dados, columns=["IDH", "Casos positivos"])

    st.markdown('### IDH X Casos positivos')
    st.vega_lite_chart(dfIdhObito, {
        "height": 300,
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'IDH', 'type': 'quantitative'},
            'y': {'field': 'Casos positivos', 'type': 'quantitative'}
        },
    }, use_container_width = True)


def vacinas_dias(dfAtual):
    dose1 = []
    dose2 = []
    date_list = []
    grouped = dfAtual.groupby(['data_vacinação'])
    for name, group in grouped:
        date_list.append(name)
        dose1.append(group[group.dose == 'DOSE 1'].shape[0])
        dose2.append(group[group.dose == 'DOSE 2'].shape[0])

    GrafDiaInfo = {'data': date_list, 'Primeira dose': dose1, 'Segunda dose': dose2}
    dfGrafDia = pd.DataFrame(GrafDiaInfo)
    dfGrafDia = dfGrafDia.set_index('data')

    st.markdown('### Mostragem dos vacinados')
    st.bar_chart(dfGrafDia)

    dose1 = np.cumsum(dose1)
    #dose2 = [x * -1 for x in dose2]
    dose2 = np.cumsum(dose2)

    GrafDiaInfo = {'data': date_list, 'Primeira dose': dose1, 'Segunda dose': dose2}
    dfGrafDia = pd.DataFrame(GrafDiaInfo)
    dfGrafDia = dfGrafDia.set_index('data')

    st.markdown('### Mostragem acumulativa dos vacinados')
    st.line_chart(dfGrafDia)


def vacinacao_grupo(dfAtual):
    grupo = []
    nGrupo1 = []
    nGrupo2 = []
    for i in dfAtual.faseDeVcinacao.value_counts().index:
        filtroGrupo = dfAtual.faseDeVcinacao == i
        dfTemp = dfAtual[filtroGrupo]

        grupo.append(i)
        nGrupo1.append(dfTemp[dfTemp.dose == 'DOSE 1'].shape[0])
        nGrupo2.append(dfTemp[dfTemp.dose == 'DOSE 2'].shape[0])
    
    GrafGrupo = {'Grupos prioritarios': grupo, 'Primeira dose': nGrupo1, 'Segunda dose': nGrupo2}
    dfGrafGrupo = pd.DataFrame(GrafGrupo)
    dfGrafGrupo = dfGrafGrupo.set_index('Grupos prioritarios')

    st.markdown('### Numero de pessoas de cada fase de vacinação')
    st.bar_chart(dfGrafGrupo)

    fase1 = ['População indígena aldeada', 
            'Idosos a partir de 60 anos institucionalizados', 
            'Trabalhadores de Saúde', 
            'Pessoas com deficiência institucionalizadas', 
            'Idosos a partir de 75 anos', 
            '', '', '', '', '', '', '']
    fase2 = ['Povos e comunidades tradicionais quilombolas', 
            'Idosos a partir de 60 anos', 
            '', '', '', '', '', '', '', '', '', '']
    fase3 = ['Pessoas com deficiência permanente grave', 
            'Pessoas com morbidades', 
            '', '', '', '', '', '', '', '', '', '']
    fase4 = ['População privada de liberdade', 
            'Funcionários do sistema de privação de liberdade', 
            'Forças de segurança e salvamento', 
            'Forças Armadas', 
            'Trabalhadores de Educação do Ensino Básico', 
            'Trabalhadores de Educação do Ensino Superior', 
            'Trabalhadores de transporte coletivo rodoviário de passageiros', 
            'Trabalhadores de transporte metroviário e ferroviário', 
            'Trabalhadores de transporte aéreo', 
            'Trabalhadores de transporte aquaviário', 
            'Caminhoneiros', 
            'Trabalhadores industriais']

    tabFases = {'Fase 1': fase1, 'Fase 2': fase2, 'Fase 3': fase3, 'Fase 4': fase4}
    tabFases = pd.DataFrame(tabFases)

    st.table(tabFases)