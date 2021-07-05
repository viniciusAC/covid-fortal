import streamlit as st
import numpy as np
import pandas as pd


def vacinas_dias(dfAtual):
    dose1 = []
    dose2 = []
    doseUni = []
    date_list = []
    grouped = dfAtual.groupby(['vacina_dataaplicacao'])
    for name, group in grouped:
        date_list.append(name)
        dose1.append(group[group.vacina_descricao_dose == '    1ª Dose'].shape[0])
        dose2.append(group[group.vacina_descricao_dose == '    2ª Dose'].shape[0])
        doseUni.append(group[group.vacina_descricao_dose == '\xa0\xa0\xa0\xa0Dose\xa0'].shape[0])

    GrafDiaInfo = {'data': date_list, 'Primeira dose': dose1, 'Segunda dose': dose2, 'Dose unica':doseUni }
    dfGrafDia = pd.DataFrame(GrafDiaInfo)
    dfGrafDia = dfGrafDia.set_index('data')

    st.markdown('### Mostragem dos vacinados')
    st.bar_chart(dfGrafDia)

    dose1 = np.cumsum(dose1)
    dose2 = np.cumsum(dose2)
    doseUni = np.cumsum(doseUni)

    GrafDiaInfo = {'data': date_list, 'Primeira dose': dose1, 'Segunda dose': dose2, 'Dose unica':doseUni }
    dfGrafDia = pd.DataFrame(GrafDiaInfo)
    dfGrafDia = dfGrafDia.set_index('data')

    st.markdown('### Mostragem acumulativa dos vacinados')
    st.line_chart(dfGrafDia)

    lista = [[dose1[-1], dose2[-1], doseUni[-1]], [dose1[-1], dose2[-1], doseUni[-1]], [dose1[-1], dose2[-1], doseUni[-1]]]
    dfInfo = pd.DataFrame(lista, columns=["Primeira dose", "Segunda dose", "Dose unica"])
    st.table(dfInfo.head(1))


def vacinacao_grupo(dfAtual):
    grupo = []
    nGrupo1 = []
    nGrupo2 = []
    nGrupoUni = []
    for i in dfAtual.faseDeVacinacao.value_counts().index:
        filtroGrupo = dfAtual.faseDeVacinacao == i
        dfTemp = dfAtual[filtroGrupo]

        grupo.append(i)
        nGrupo1.append(dfTemp[dfTemp.vacina_descricao_dose == '    1ª Dose'].shape[0])
        nGrupo2.append(dfTemp[dfTemp.vacina_descricao_dose == '    2ª Dose'].shape[0])
        nGrupoUni.append(dfTemp[dfTemp.vacina_descricao_dose == '\xa0\xa0\xa0\xa0Dose\xa0'].shape[0])
    
    GrafGrupo = {'Grupos prioritarios': grupo, 'Primeira dose': nGrupo1, 'Segunda dose': nGrupo2, 'Dose unica': nGrupoUni }
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