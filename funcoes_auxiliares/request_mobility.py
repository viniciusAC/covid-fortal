import requests
import pandas as pd
import io

from funcoes_auxiliares.crawler_mobility import *


def filtrar_fort(dfAtual):
    filtroLocal = (dfAtual.sub_region_2 == 'Fortaleza')
    dfAtual = dfAtual[filtroLocal]
    return dfAtual


def del_col(dfAtual):
    colunas = ['date', 'retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline', 
                'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline',
                'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline']
    for i in dfAtual.columns.to_list():
        if i not in colunas:
            dfAtual.drop(columns=[i], inplace=True)
    return dfAtual


def request_mobilidade():
    link = crawler()
    print('Solicitando dados')
    data = requests.get(link, stream=True).content
    data = pd.read_csv(io.StringIO(data.decode('utf-8')), sep=',')
    print('Tratando dados')
    data = filtrar_fort(data)
    data = del_col(data)
    data.to_csv('Base_de_dados/mobilidade.csv', sep=';')
    print('######################################################################################################')