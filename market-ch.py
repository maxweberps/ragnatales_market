from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import re, time


def converter_para_intero(preco_str):
    numeros = re.findall(r'\d+', preco_str)
    num_concatenado = ''.join(numeros)
    preco_int = int(num_concatenado)
    return preco_int


# CADASTRO DE ALETAS DE PREÇO
item = ''
preco_alerta = 0
itens_monitorados = {}
cont = 0
print('--- CADASTRO DE ALERTAS DE PREÇO ---\nDigite "sair" para encerrar cadastro')
while True:
    cont += 1
    item = input(f'Nome do item {cont}: ')
    if item == 'sair':
        break
    else:
        preco_alerta = float(input(f'Preço alerta: '))
        itens_monitorados[item] = [preco_alerta, 1000000000]

# INICIALIZAR NAVEGADOR
servico = Service(ChromeDriverManager().install())
nav = webdriver.Chrome(service=servico)
# espera 10 segundo tempo de carregamento inicial do site
nav.implicitly_wait(10)

# abre zap (login)
nav.get('https://web.whatsapp.com')
time.sleep(30)
# abre market
nav.get('https://ragnatales.com.br/market')
time.sleep(10)
sessao = 0
# entra no loop de monitorar o preço do item
while True:
    sessao += 1
    print(f'--- SESSÃO DE PESQUISA {sessao} ---')
    for item in itens_monitorados:
        # insere o nome do item na barra de pesquisa
        print(f'> Coletando preço atual do item {item}...')
        nav.find_element('xpath',
                         '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/label/div/div[1]/input').clear()  # limpa caixa de pesquisa
        nav.find_element('xpath', '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/label/div/div[1]/input').send_keys(
            item)
        time.sleep(3)
        # envia comando enter para pesquisa
        nav.find_element('xpath', '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/label/div/div[1]/input').send_keys(
            Keys.ENTER)
        time.sleep(8)
        # coleta preço atual do item
        preco_atual = converter_para_intero(nav.find_element('xpath',
                                                             '//*[@id="app"]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/span').text)
        print(f'Preço coletado: {preco_atual}z')
        itens_monitorados[item][1] = preco_atual
        print(
            f'> Resumo:\nItem: {item}\nPreço alerta: {itens_monitorados[item][0]:.0f}z\nPreço atual: {itens_monitorados[item][1]}z')
        print('> Comparando preço atual com alerta...')
        if itens_monitorados[item][1] <= itens_monitorados[item][0]:
            print(f'> Preço alerta do item {item} alcançado!')
            print(f'> Enviando notificação via whatsapp...')
            nav.get('https://web.whatsapp.com')
            time.sleep(5)
            # clicar na lupa
            # nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div/button/div[2]/span').click()
            nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p').send_keys("Max Silva TI")
            time.sleep(2)
            nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p').send_keys(Keys.ENTER)
            print('> Notificação enviada.')
            time.sleep(1)

            # escrever a mensagem
            nav.find_element('xpath',
                             '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').send_keys(
                f'Preço alerta do item {item} alcançado! Preço atual: {itens_monitorados[item][1]}z')
            time.sleep(1)
            nav.find_element('xpath',
                             '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').send_keys(
                Keys.ENTER)
            time.sleep(1)
            nav.get('https://ragnatales.com.br/market')
            time.sleep(10)
        else:
            print(f'> Preço alerta do item {item} não alcançado.')

    nav.refresh()
    time.sleep(120)  # intervalo de tempo entre as sessões de pesquisa
