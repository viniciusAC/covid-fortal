import streamlit as st
import numpy as np
import pandas as pd
import datetime
import pydeck as pdk
from pydeck.types import String


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
    
    dfIdhObito = pd.DataFrame(dadosObito, columns=["IDH", "Obitos"])

    st.markdown('### IDH X Obitos')
    st.vega_lite_chart(dfIdhObito, {
        "height": 300,
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'IDH', 'type': 'quantitative'},
            'y': {'field': 'obitos', 'type': 'quantitative'}
        },
    }, use_container_width = True)

    dfIdhConfirmado = pd.DataFrame(dados, columns=["IDH", "Casos positivos"])

    st.markdown('### IDH X Casos positivos')
    st.vega_lite_chart(dfIdhConfirmado, {
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
    grouped = dfAtual.groupby(['vacina_dataaplicacao'])
    for name, group in grouped:
        date_list.append(name)
        dose1.append(group[group.vacina_descricao_dose == '    1ª Dose'].shape[0])
        dose2.append(group[group.vacina_descricao_dose == '    2ª Dose'].shape[0])

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
    for i in dfAtual.faseDeVacinacao.value_counts().index:
        filtroGrupo = dfAtual.faseDeVacinacao == i
        dfTemp = dfAtual[filtroGrupo]

        grupo.append(i)
        nGrupo1.append(dfTemp[dfTemp.vacina_descricao_dose == '    1ª Dose'].shape[0])
        nGrupo2.append(dfTemp[dfTemp.vacina_descricao_dose == '    2ª Dose'].shape[0])
    
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

def mapa(dfAtual, bairro_info):
    dadosObito = []
    dadosConfirmado = []
    for i in dfAtual.bairroCaso.value_counts().index:
        if i == 'Indeterminado' or bairro_info.loc[i][1] == 0:
            continue
        filtroBairro = dfAtual.bairroCaso == i
        dfTemp = dfAtual[filtroBairro]
        dadosObito.append([bairro_info.loc[i][2], bairro_info.loc[i][3],
                    (dfTemp[dfTemp.obitoConfirmado == 'Verdadeiro'].shape[0]/bairro_info.loc[i][1])*100])
        dadosConfirmado.append([bairro_info.loc[i][2], bairro_info.loc[i][3], 
                    (dfTemp[dfTemp.resultadoFinalExame == 'Positivo'].shape[0]/bairro_info.loc[i][1])*100])
    
    dfIdhObito = pd.DataFrame(dadosObito, columns=["lat", "lon", "Obitos"])
    dfIdhConfirmado = pd.DataFrame(dadosConfirmado, columns=["lat", "lon", "Casos positivos"])

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=-3.7789976,
            longitude=-38.5401627,
            zoom=10.5,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'HeatmapLayer',
                data=dfIdhObito,
                get_position='[lon, lat]',
                opacity=0.5,
                aggregation=String('MEAN'),
                get_weight="Obitos"
            ),
        ],
    ))


def tipo_vac(dfAtual):
    grupo = []
    nVac = []
    for i in dfAtual.vacina_nome.value_counts().index:
        filtroGrupo = dfAtual.vacina_nome == i
        dfTemp = dfAtual[filtroGrupo]

        grupo.append(i)
        nVac.append(dfTemp.shape[0])
    
    GrafVac = {'Vacina': grupo, 'Doses aplicadas': nVac}
    dfGrafVac = pd.DataFrame(GrafVac)
    dfGrafVac = dfGrafVac.set_index('Vacina')

    st.markdown('### Quantidade de cada vacina aplicada')
    st.bar_chart(dfGrafVac, height= 500)