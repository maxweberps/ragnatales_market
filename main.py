from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
import re

servico = Service(GeckoDriverManager().install())
navegador = webdriver.Firefox(service=servico)

# espera 10 segundo tempo de carregamento inicial do site
navegador.implicitly_wait(10)

# abre o navegador
navegador.get('https://ragnatales.com.br/market')
# insere o nome do intem na barra de pesquisa
navegador.find_element('xpath', '/html/body/div[1]/div/div/div[2]/div/div[2]/div[1]/label/div/div[1]/input').send_keys(
    "Botas Veteranas")
# envia comando enter para pesquisa
navegador.find_element('xpath', '/html/body/div[1]/div/div/div[2]/div/div[2]/div[1]/label/div/div[1]/input').send_keys(
    Keys.ENTER)

# coleto o preco do item mais barato
texto = navegador.find_element('xpath',
                               '/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/span').text
print(texto)

# converte em inteiro
numeros = re.findall(r'\d+', texto)
num_concatenado = ''.join(numeros)
print(num_concatenado)
preco = int(num_concatenado)
print(preco)
print(type(preco))
