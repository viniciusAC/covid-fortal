import numpy as np
import pandas as pd
import datetime
import Levenshtein

from funcoes_auxiliares.otimizacao import *


def delete_wrong_dates(df_atual):
    print('Excluindo datas bsurdas')
    df_atual.idadeCaso = df_atual.idadeCaso.replace(range(101,1001), float("nan"))
    df_atual.loc[df_atual['idadeCaso'] == float("nan"), 'faixaEtaria'] = 'Sem Informacao'
    df_atual.faixaEtaria = df_atual.faixaEtaria.fillna('Sem Informacao')
    dates = ['dataResultadoExame', 'dataInicioSintomas', 'dataColetaExame']
    optimize2(df_atual, dates)
    return df_atual


def remove_columns(df_atual):
    print('Removendo colunas desnecessarias')
    columns_atuais = df_atual.columns.to_list()
    columns = ['codigoPaciente', 'municipioPaciente', 'bairroPaciente', 'sexoPaciente', 'dataResultadoExame', 'resultadoFinalExame',
            'dataInicioSintomas', 'dataColetaExame', 'racaCorPaciente', 'obitoConfirmado', 'idadePaciente']

    for i in columns_atuais:
        if i not in columns:
            df_atual = df_atual.drop([i], axis=1)
    return df_atual


def create_faixaEtaria(df_atual):
    print('Criando coluna de faixa etaria')
    df_atual.idadeCaso = pd.to_numeric(df_atual.idadeCaso)

    df_atual.loc[(df_atual.idadeCaso >= 0) & (df_atual.idadeCaso <= 4), 'faixaEtaria'] = '00 a 04 anos'
    df_atual.loc[(df_atual.idadeCaso >= 5) & (df_atual.idadeCaso <= 9), 'faixaEtaria'] = '05 a 09 anos'
    df_atual.loc[(df_atual.idadeCaso >= 10) & (df_atual.idadeCaso <= 14), 'faixaEtaria'] = '10 a 14 anos'
    df_atual.loc[(df_atual.idadeCaso >= 15) & (df_atual.idadeCaso <= 19), 'faixaEtaria'] = '15 a 19 anos'
    df_atual.loc[(df_atual.idadeCaso >= 20) & (df_atual.idadeCaso <= 24), 'faixaEtaria'] = '20 a 24 anos'
    df_atual.loc[(df_atual.idadeCaso >= 25) & (df_atual.idadeCaso <= 29), 'faixaEtaria'] = '25 a 29 anos'
    df_atual.loc[(df_atual.idadeCaso >= 30) & (df_atual.idadeCaso <= 34), 'faixaEtaria'] = '30 a 34 anos'
    df_atual.loc[(df_atual.idadeCaso >= 35) & (df_atual.idadeCaso <= 39), 'faixaEtaria'] = '35 a 39 anos'
    df_atual.loc[(df_atual.idadeCaso >= 40) & (df_atual.idadeCaso <= 44), 'faixaEtaria'] = '40 a 44 anos'
    df_atual.loc[(df_atual.idadeCaso >= 45) & (df_atual.idadeCaso <= 49), 'faixaEtaria'] = '45 a 49 anos'
    df_atual.loc[(df_atual.idadeCaso >= 50) & (df_atual.idadeCaso <= 54), 'faixaEtaria'] = '50 a 54 anos'
    df_atual.loc[(df_atual.idadeCaso >= 55) & (df_atual.idadeCaso <= 59), 'faixaEtaria'] = '55 a 59 anos' 
    df_atual.loc[(df_atual.idadeCaso >= 60) & (df_atual.idadeCaso <= 64), 'faixaEtaria'] = '60 a 64 anos'
    df_atual.loc[(df_atual.idadeCaso >= 65) & (df_atual.idadeCaso <= 69), 'faixaEtaria'] = '65 a 69 anos'
    df_atual.loc[(df_atual.idadeCaso >= 70) & (df_atual.idadeCaso <= 74), 'faixaEtaria'] = '70 a 74 anos'
    df_atual.loc[(df_atual.idadeCaso >= 75) & (df_atual.idadeCaso <= 79), 'faixaEtaria'] = '75 a 79 anos'
    df_atual.loc[(df_atual.idadeCaso >= 80), 'faixaEtaria'] = '80 ou mais'
    df_atual.faixaEtaria.fillna('Sem Informacao', inplace=True)

    return df_atual


def filter_muni(df_atual):
    print('Filtrando dados para Fortaleza')
    correcoes = {}
    for i in df_atual.municipioCaso.value_counts().index:
        lev = Levenshtein.distance(i,'FORTALEZA')
        if lev < 4:
            correcoes[i] = 'FORTALEZA'
            dist = lev
    for i in range(len(list(correcoes))):
        df_atual.municipioCaso = df_atual.municipioCaso.replace(list(correcoes)[i], correcoes[list(correcoes)[i]])

    filtro = (df_atual.municipioCaso == 'FORTALEZA')
    df_atual = df_atual[filtro]
    df_atual = df_atual.drop(columns=['municipioCaso'])
    return df_atual


def date_correction(df_atual):
    print('Corrigindo datas')
    anoDeCont = []
    dataCaso = []
    result = df_atual.dataResultadoExame.to_list()
    sintomas = df_atual.dataInicioSintomas.to_list()
    exame = df_atual.dataColetaExame.to_list()

    for i in range(len(result)):
        if sintomas[i].year == 2020:
            anoDeCont.append('2020')
            dataCaso.append(sintomas[i])
        elif sintomas[i].year == 2021:
            anoDeCont.append('2021')
            dataCaso.append(sintomas[i])
        else:
            if exame[i].year == 2020:
                anoDeCont.append('2020')
                dataCaso.append(exame[i])
            elif exame[i].year == 2021:
                anoDeCont.append('2021')
                dataCaso.append(exame[i])
            else:
                if result[i].year == 2020:
                    anoDeCont.append('2020')
                    dataCaso.append(result[i])
                elif result[i].year == 2021:
                    anoDeCont.append('2021')
                    dataCaso.append(result[i])
                else:
                    anoDeCont.append('Excluir')
                    dataCaso.append('Excluir')
    df_atual['anoDeContagio'] = anoDeCont

    for i in df_atual.columns.to_list(): 
        if i[0]+i[1]+i[2]+i[3] == 'data':
            df_atual = df_atual.drop(columns=i)
    df_atual['dataCaso'] = dataCaso

    indexNames = df_atual[ (df_atual['dataCaso'] == 'Excluir') |
                            (df_atual['anoDeContagio'] == 'Excluir') ].index
    df_atual.drop(indexNames , inplace=True)

    return df_atual


def wrong_values(df_atual):
    print('Tratando valores errados')

    df_atual.bairroCaso.fillna('Indeterminado', inplace=True)

    df_atual.sexoCaso.replace('INDEFINIDO', df_atual.sexoCaso.value_counts().index[0], inplace=True)
    df_atual.sexoCaso.replace('I', df_atual.sexoCaso.value_counts().index[0], inplace=True)
    df_atual.sexoCaso.replace('N.I.', df_atual.sexoCaso.value_counts().index[0], inplace=True)
    df_atual.sexoCaso.fillna(df_atual.sexoCaso.value_counts().index[0], inplace=True)

    df_atual.resultadoFinalExame.replace('Provável', 'Caso suspeito', inplace=True)
    df_atual.resultadoFinalExame.replace('Inconclusivo', 'Caso suspeito', inplace=True)
    df_atual.resultadoFinalExame.replace('Em Análise', 'Caso suspeito', inplace=True)
    df_atual.resultadoFinalExame.fillna('Caso suspeito', inplace=True)
    # df_atual.resultadoFinalExame.replace('Negativo', 'Z Negativo', inplace=True)

    df_atual.racaCor.replace('Parda.0', 'Parda', inplace=True)
    df_atual.racaCor.replace('.0', 'Sem Informacao', inplace=True)
    df_atual.racaCor.fillna('Sem Informacao', inplace=True)
    df_atual.racaCor.replace('Branca.0', 'Branca', inplace=True)
    df_atual.racaCor.replace('Preta.0', 'Preta', inplace=True)
    df_atual.racaCor.replace('Amarela.0', 'Amarela', inplace=True)
    df_atual.racaCor.replace('Indígena.0', 'Indígena', inplace=True)

    df_atual.obitoConfirmado.replace(True, 'Verdadeiro', inplace=True)
    df_atual.obitoConfirmado.replace(False, 'Falso', inplace=True)
    df_atual.obitoConfirmado.fillna('Falso', inplace=True)

    return df_atual


def correction_bairro(df_atual, bairro_info):
    print('Corrigindo bairros')
    correcoes = {}
    bairros_cor = bairro_info.index
    for i in df_atual.bairroCaso.value_counts().index:
        dist = 20
        for j in bairros_cor:
            lev = Levenshtein.distance(i,j)
            if dist == 20 and lev < 3:
                correcoes[i] = j
                dist = lev
            elif dist < 20 and lev < dist:
                correcoes[i] = j
                dist = lev

    for i in range(len(list(correcoes))):
        df_atual.bairroCaso = df_atual.bairroCaso.replace(list(correcoes)[i], correcoes[list(correcoes)[i]])

    filtro = ~ df_atual.bairroCaso.isin(bairros_cor)
    df_atual.loc[filtro, 'bairroCaso'] = 'Indeterminado'

    return df_atual


def calculate_infection(df_atual, bairro_info):
    print('Calculando metricas dos bairros')
    filtro = (df_atual.anoDeContagio == '2020')
    df2020 = df_atual[filtro]
    filtro2 = ((df2020.resultadoFinalExame == 'Positivo') | (df2020.resultadoFinalExame == 'Suspeito'))
    df2020 = df2020[filtro2]

    filtro = (df_atual.anoDeContagio == '2021')
    df2021 = df_atual[filtro]
    filtro2 = ((df2021.resultadoFinalExame == 'Positivo') | (df2021.resultadoFinalExame == 'Suspeito'))
    df2021 = df2021[filtro2]

    filtro2 = ((df_atual.resultadoFinalExame == 'Positivo') | (df_atual.resultadoFinalExame == 'Suspeito'))
    df_limpa = df_atual[filtro2]

    razao2020 = {}
    razao2021 = {}
    count = 0

    bairroValues2020 = df2020.bairroCaso.value_counts()
    bairroValues2021 = df2021.bairroCaso.value_counts()

    for i in bairro_info.index.to_list():
        if bairro_info.loc[i]['populaçao em 2010[8]'] != 0:
            razao2020[i] = bairroValues2020[i] / bairro_info.loc[i]['populaçao em 2010[8]']
            razao2021[i] = bairroValues2021[i] / bairro_info.loc[i]['populaçao em 2010[8]']

    razao = {}
    for i in razao2020.keys():
        razao[i] = razao2020[i] + razao2021[i]

    razao2020 = sorted(razao2020.items(), key=lambda kv: kv[0])
    razao2021 = sorted(razao2021.items(), key=lambda kv: kv[0])
    razao = sorted(razao.items(), key=lambda kv: kv[1])

    razao2020 = pd.DataFrame(razao2020,columns=['Bairros', 'Razao_2020'])
    razao2020 = razao2020.set_index('Bairros')
    razao2021 = pd.DataFrame(razao2021,columns=['Bairros', 'Razao_2021'])
    razao2021 = razao2021.set_index('Bairros')
    razao = pd.DataFrame(razao,columns=['Bairros', 'Razao'])
    razao = razao.set_index('Bairros')
    bairro_info = pd.concat([bairro_info, razao2020, razao2021, razao], axis=1)

    bairro_info.to_csv('Base de dados/dados_bairros+.csv', sep=',')

def processing_new_rows(df_atual):
    df_atual = remove_columns(df_atual)

    df_atual.rename(columns={"codigoPaciente": "identificadorCaso", "municipioPaciente": "municipioCaso",
                            "bairroPaciente": "bairroCaso",  "sexoPaciente": "sexoCaso", "racaCorPaciente": "racaCor", 
                            "obitoConfirmado": "obitoConfirmado", "idadePaciente": "idadeCaso"}, inplace=True)
    
    df_atual = create_faixaEtaria(df_atual)
    df_atual = delete_wrong_dates(df_atual)
    df_atual = filter_muni(df_atual)
    df_atual = date_correction(df_atual)
    df_atual = wrong_values(df_atual)

    bairro_info = pd.read_csv(f'Base de dados/dados_bairros.csv', sep=',')
    bairro_info.Bairros	= bairro_info.Bairros.str.upper()
    bairro_info = bairro_info.set_index('Bairros')

    df_atual = correction_bairro(df_atual, bairro_info)

    return df_atual

def add_rows(df_atual):
    data = pd.read_csv('Base de dados/dados_limpos.csv', sep=';')
    data = data.drop(['Unnamed: 0'], axis=1)
    data['dataCaso'] = pd.to_datetime(data['dataCaso'])
    data['dataCaso'] = data['dataCaso'].dt.date

    data = data.append(df_atual, ignore_index=True)
    data.drop_duplicates(keep=False,inplace=True,ignore_index=True)

    data.to_csv('Base de dados/dados_limpos.csv', sep=';')

    

