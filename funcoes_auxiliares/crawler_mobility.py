from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)

    erros_seguidos = 0

    while(True):
        try:
            if erros_seguidos > 5:
                print()
                print("Muitos erros consecutivos, reniciando função ####################################################################")
                print()
                return True, ''

            driver.get("https://www.google.com.br/covid19/mobility/index.html?hl=pt-BR")
            time.sleep(2)
            link = driver.find_element_by_xpath('/html/body/div[1]/section[3]/div[2]/div/div[1]/p[3]/a[1]')
            link = link.get_attribute("href")
            print('Operação concluida #####################################################################')
            break

        except Exception as e:
            erros_seguidos = erros_seguidos + 1
            print(e)

    driver.quit()
    return False, link

def crawler():
    continua = True
    while continua:
        print('Iniciando operação #####################################################################')
        try:
            continua, link = main()
        except Exception as e:
            print(e)
            continua = True
    return link