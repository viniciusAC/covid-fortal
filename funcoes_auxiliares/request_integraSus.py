import requests
import pandas as pd
import io
import zipfile
import os
import shutil
import glob

from funcoes_auxiliares.pre_proces import *

def resquest_new_rows():
    print('solicitando dados')
    r = requests.get("http://download-integrasus.saude.ce.gov.br/download", stream=True)

    print('extraindo dados')
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall('Base_de_dados/zip/')

    files = []
    for file in glob.glob('Base_de_dados/zip/casos_coronavirus_20*.csv'):
        files.append(file[18:])

    print('Criando nova base')
    base = pd.read_csv(f'Base_de_dados/zip/{files.pop()}', sep=';')
    optimize2(base)
    for i in files:
        partial = pd.read_csv(f'Base_de_dados/zip/{i}', sep=';')
        optimize2(partial)
        base = base.append(partial, ignore_index=True)

    shutil.rmtree('Base_de_dados/zip/')

    return base


def pre_proces_new_rows(dfAtual):
    print('Adicionando novos dados aos anteriores')
    processing_new_rows(dfAtual)