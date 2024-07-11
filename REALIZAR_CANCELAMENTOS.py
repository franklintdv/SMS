import pandas as pd
import time
import pyautogui
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Nome do arquivo de saída
output_file = 'pendentes.csv'

# Abrir o navegador e acessar o site do SISREG.
driver = webdriver.Chrome()
driver.get("https://sisregiii.saude.gov.br/")

# Adicionando informações de login e senha.
user = '5408989FRANKLIN'
password = '555555Aa'
driver.find_element(By.NAME, "usuario").send_keys(user)
driver.find_element(By.NAME, "senha").send_keys(password)
driver.find_element(By.NAME, "entrar").click()


# Abrir o arquivo pendentes.csv para leitura
with open(output_file, mode='r', encoding='utf-8') as csvfile:
    # Criar um leitor de CSV
    reader = csv.reader(csvfile, delimiter=';')
    
    # Iterar sobre as linhas do arquivo
    for row in reader:
        solicitacao = row[0].strip()
        print(f"Processando solicitacao: {solicitacao}")
        # Entrar na página de confirmação.
        driver.get("https://sisregiii.saude.gov.br/cgi-bin/cons_verificar")
        driver.find_element(By.NAME, "co_solic").clear()
        driver.find_element(By.NAME, "co_solic").send_keys(solicitacao)
        driver.find_element(By.NAME, "consulta").click()
        time.sleep(1)
        try:
            driver.find_element(By.NAME, "chk_0").click()
            justificativa_cancelamento = 'Paciente não compareceu ao exame.'
            driver.find_element(By.NAME, "justificativa").send_keys(justificativa_cancelamento)
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="main_page"]/form/center/table[3]/tbody/tr[1]/td/table/tbody/tr[4]/td/input').click()
            # Wait for the alert to appear
            alert = None
            while not alert:
                try:
                    alert = driver.switch_to.alert
                except:
                     time.sleep(1)
            # Assuming "OK" is the only button on the alert
            alert.accept()
            time.sleep(1)
        except:
            time.sleep(1)
            continue 
           