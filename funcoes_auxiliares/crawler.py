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

    vacinados.to_csv('Base de dados/vacinados.csv', sep=';')

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
    driver.get("https://vacinacao.sms.fortaleza.ce.gov.br/pesquisa/atendidos")

    time.sleep(5)
    button = driver.find_elements_by_xpath('//*[@id="tableGrid"]/tfoot/tr/td/div/ul/li/a')
    button[0].click()

    page_arg = f'$("#formBusca #activePage").val({pagina}); buscar();'
    time.sleep(5)
    button = driver.find_elements_by_xpath('//*[@id="tableGrid"]/tfoot/tr/td/div/ul/li[2]/a')
    driver.execute_script(f"document.querySelector('#tableGrid > tfoot > tr > td > div > ul > li:nth-child(2) > a').setAttribute('onclick','{page_arg}');", button)
    button[0].click()

    erros_seguidos = 0

    while(True):
        try:
            if erros_seguidos > 5:
                print()
                print("Muitos erros consecutivos, reniciando função")
                print()
                return True
            if pagina % 25 == 0:
                salvar(pagina, linha, vacinados)
            print(pagina)
            time.sleep(7)
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
            print('Função interrompida #####################################################################')

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
    print("Dados atualizados")