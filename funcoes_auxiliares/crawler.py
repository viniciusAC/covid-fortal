from selenium import webdriver
import time
import pandas as pd
import os
from selenium.webdriver.chrome.options import Options
import sys

from funcoes_auxiliares.otimizacao import *

def salvar(pagina, linha, vacinados):
    print()
    print("Salvando registros")
    print()
    progresso = pd.DataFrame(columns=['pagina', 'linha'])
    new_row = {'pagina': pagina, 'linha': linha}
    progresso = progresso.append(new_row, ignore_index=True)
    progresso.to_csv('Base de dados/progresso_crawler.csv', sep=';')

    vacinados.drop_duplicates(keep=False,inplace=True,ignore_index=True)
    vacinados.to_csv('Base de dados/vacinados.csv', sep=';')

def prep_pagina(driver, pagina):
    driver.get("https://vacinacao.sms.fortaleza.ce.gov.br/pesquisa/atendidos")

    time.sleep(5)
    button = driver.find_elements_by_xpath('//*[@id="tableGrid"]/tfoot/tr/td/div/ul/li/a')
    button[0].click()

    page_arg = f'$("#formBusca #activePage").val({pagina}); buscar();'
    time.sleep(5)
    button = driver.find_elements_by_xpath('//*[@id="tableGrid"]/tfoot/tr/td/div/ul/li[2]/a')
    driver.execute_script(f"document.querySelector('#tableGrid > tfoot > tr > td > div > ul > li:nth-child(2) > a').setAttribute('onclick','{page_arg}');", button)
    button[0].click()

def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    vacinados = pd.read_csv('Base de dados/vacinados.csv', sep=';')
    vacinados = vacinados.drop(['Unnamed: 0'], axis=1)

    atual = pd.read_csv('Base de dados/progresso_crawler.csv', sep=';')
    atual = atual.drop(['Unnamed: 0'], axis=1)

    ult_pagina = atual.pagina.value_counts().index[0]
    pagina = ult_pagina
    ult_linha = atual.linha.value_counts().index[0]
    linha = -1


    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

    prep_pagina(driver, pagina)

    erros_seguidos = 0

    while(True):
        try:
            if erros_seguidos > 5:
                print()
                print("Muitos erros consecutivos, reniciando função ####################################################################")
                print()
                return True
            if pagina % 25 == 0:
                salvar(pagina, linha, vacinados)
            if pagina % 50 == 0:
                print()
                print("Reiniciando driver por questão de otimização ########################################################################")
                print()
                driver.quit()
                driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
                prep_pagina(driver, pagina)
            print(pagina)
            time.sleep(5)
            results = driver.find_elements_by_xpath('//*[@id="row_undefined"]')

            for j in results:
                linha = linha + 1
                if pagina == ult_pagina and linha <= ult_linha:
                    continue
                colunas = j.find_elements_by_tag_name('td')
                new_row = {'nome': colunas[0].text, 'grupo_prioritario': colunas[1].text, 'data_vacinação': colunas[2].text, 'dose': colunas[4].text}
                vacinados = vacinados.append(new_row, ignore_index=True)

            
            button = driver.find_elements_by_xpath('//*[@id="tableGrid"]/tfoot/tr/td/div/ul/li[2]/a')
            if len(button) == 0:
                button = driver.find_elements_by_xpath('//*[@id="tableGrid"]/tfoot/tr/td/div/ul/li/a')
            button[0].click()
            if len(results) == 30:
                pagina = pagina + 1
                linha = -1
                erros_seguidos = 0
            else:
                break
        except KeyboardInterrupt:
            print()
            print('Função interrompida #####################################################################')
            print()

            driver.quit()

            salvar(pagina, linha, vacinados)

            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        except Exception as e:
            erros_seguidos = erros_seguidos + 1
            print(e)

    driver.quit()
    salvar(pagina, linha, vacinados)
    return False

def vac_fase():
    dicFase = {'MÉDICO': 'Fase 1',
        '80 ANOS OU MAIS': 'Fase 1',
        'TÉC. DE ENFERMAGEM': 'Fase 1',
        '75 A 79 ANOS': 'Fase 1',
        'ENFERMEIRO(A)': 'Fase 1',
        'AUX.DE ENFERMAGEM': 'Fase 1',
        'ODONTOLOGISTA': 'Fase 1',
        'FISIOTERAPEUTAS': 'Fase 1',
        'FARMACÊUTICO': 'Fase 1',
        'PSICÓLOGO': 'Fase 1',
        'TÉC. DE ODONTOLOGIA': 'Fase 1',
        'NUTRICIONISTA': 'Fase 1',
        'BIOMÉDICO': 'Fase 1',
        'PORTADOR DE DEFICIÊNCIA INSTITUC.': 'Fase 1',
        'IDOSOS INSTITUCIONALIZADOS': 'Fase 1',
        'INDÍGENAS': 'Fase 1',
        '65 A 69 ANOS': 'Fase 2',
        '70 A 74 ANOS': 'Fase 2',
        '60 A 64 ANOS': 'Fase 2',
        'HIPERTENSÃO GRAVE': 'Fase 3',
        'DIABETES': 'Fase 3',
        'DOENÇAS CARDIO-CEREBROVASCULARES': 'Fase 3',
        'OBESIDADE GRAVE': 'Fase 3',
        'DOENÇA RENAL': 'Fase 3',
        'CÂNCER': 'Fase 3',
        'DEFICIÊNCIA GRAVE': 'Fase 3',
        'SÍNDROME DE DOWN': 'Fase 3',
        'INDIVÍDUOS TRANSPLANTADOS DE ÓRGÃO SÓLIDO': 'Fase 3',
        'ANEMIA FALCIFORME': 'Fase 3',
        'RECEPCIONISTA': 'Fase 4',
        'POPULAÇÃO GERAL': 'Fase 4',
        'ASSISTENTE SOCIAL': 'Fase 4',
        'AUX. LIMPEZA': 'Fase 4',
        'POLICIAL MILITAR': 'Fase 4',
        'SEGURANÇA': 'Fase 4',
        'FONOAUDIÓLOGO': 'Fase 4',
        'TERAPEUTA OCUP.': 'Fase 4',
        'BOMBEIRO MILITAR': 'Fase 4',
        'EDUCADOR FÍSICO': 'Fase 4',
        'POLICIAL CIVIL': 'Fase 4',
        'MOTORISTA DE AMBULÂNCIA': 'Fase 4',
        'PORTADOR DE DPOC': 'Fase 4',
        'GUARDA MUNICIPAL': 'Fase 4',
        'CUIDADOR DE IDOSOS': 'Fase 4',
        'MED. VETERINÁRIO': 'Fase 4',
        'POLICIAL ROD. FEDERAL': 'Fase 4',
        'MILITARES': 'Fase 4',
        'BIÓLOGO': 'Fase 4',
        'ESTUDANTE': 'Fase 4',
        'POLICIAL FEDERAL': 'Fase 4',
        'COZINHEIRO E AUXILIARES': 'Fase 4',
        'ACAMPADOS': 'Fase 4',
        'ENSINO SUPERIOR': 'Fase 4',
        'ENSINO BÁSICO': 'Fase 4',
        'AQUAVIÁRIO': 'Fase 4',
        'BOMBEIRO CIVIL': 'Fase 4',
        'DOULA/PARTEIRA': 'Fase 4',
        'FUNCIONÁRIO DO SIST. FUNERÁRIO': 'Fase 4',
        'CAMINHONEIRO': 'Fase 4',
        'EXÉRCITO': 'Fase 4',
        'FORÇA AÉREA': 'Fase 4',
        'OUTROS': 'Outro'
    }

    vacinados = pd.read_csv('Base de dados/vacinados.csv', sep=';')
    vacinados = vacinados.drop(['Unnamed: 0'], axis=1)
    vacinados = vacinados.drop(['faseDeVcinacao'], axis=1)

    for i in range(len(list(dicFase))):
        vacinados.loc[vacinados.grupo_prioritario == list(dicFase)[i], 'faseDeVcinacao'] = dicFase[list(dicFase)[i]]

    vacinados.drop_duplicates(keep=False,inplace=True,ignore_index=True)
    vacinados.to_csv('Base de dados/vacinados.csv', sep=';')    


def crawler():
    continua = True
    while continua:
        print('Iniciando operação #####################################################################')
        try:
            continua = main()
        except:
            continua = True
        if continua:
            time.sleep(15)
    vac_fase()
    print("Dados atualizados")