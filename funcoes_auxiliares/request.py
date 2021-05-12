import requests
import pandas as pd
import io
import datetime
from datetime import timedelta

from funcoes_auxiliares.pre_proces import *

def resquest_new_rows():
    atual = pd.read_csv('Base de dados/ult_data_request.csv', sep=';')
    atual = atual.drop(['Unnamed: 0'], axis=1)
    atual['data'] = pd.to_datetime(atual['data'])
    atual['data'] = atual['data'].dt.date

    date = atual.data.value_counts().index[0]
    date = date - timedelta(days=7)
    todayDate = datetime.date.today()

    continua = True

    while continua:
        try:
            print('Solicitando novos dados')
            r = requests.get(f"https://indicadores.integrasus.saude.ce.gov.br/api/casos-coronavirus?dataInicio={date}&dataFim={todayDate}")
            data = pd.json_normalize(r.json())
            continua = False
        except Exception as e:
            erros_seguidos = erros_seguidos + 1
            print(e)

    return data


def pre_proces_new_rows(dfAtual):
    print('Adicionando novos dados aos anteriores')
    dfAtual = processing_new_rows(dfAtual)
    add_rows(dfAtual)

    todayDate = datetime.date.today()
    progresso = pd.DataFrame(columns=['data'])
    new_row = {'data': todayDate}
    progresso = progresso.append(new_row, ignore_index=True)
    progresso.to_csv('Base de dados/ult_data_request.csv', sep=';')