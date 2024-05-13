#Bibliotecas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re
#Criação navegador:
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#Importar/Visualizar a base de dados
produtos_df = pd.read_excel('buscas.xlsx')
print(produtos_df)
def buscar_google(navegador, produto, termos_banidos, preco_minimo, preco_maximo):
    ##GOOGLE:
    #Entrar no google
    link = "https://www.google.com/webhp?hl=pt-BR&sa=X&ved=0ahUKEwjUn-eMy4mGAxV5LbkGHQFiAgsQPAgJ"
    navegador.get(link)

    #Pesquisar pelo produto
    produto = produto
    produto = produto.lower()
    lista_termos_nome = produto.split(' ')
    termos_banidos = termos_banidos
    termos_banidos = termos_banidos.lower()
    lista_termos_banidos = termos_banidos.split(' ')
    preco_minimo = preco_minimo
    preco_maximo = preco_maximo

    barra_pesquisa = navegador.find_element('xpath', '//*[@id="APjFqb"]')
    barra_pesquisa.send_keys(produto, Keys.ENTER)

    #Entrar na aba shopping
    while len(navegador.find_elements('xpath', '//*[@id="hdtb-sc"]/div/div/div[1]/div/div[2]/a') == 0):
        time.sleep(1)
    elemento = navegador.find_element('xpath', '//*[@id="hdtb-sc"]/div/div/div[1]/div/div[2]/a')
    link = elemento.get_attribute('href')  # Obter o link do elemento
    navegador.get(link)  # Acessar o link

    #Pegar as informações do produto
    lista_resultados = navegador.find_elements('class name', 'sh-dgr__content')
    #Para cada resultado -> 1 nome, 1 link e 1 preco
    lista_produtos = []
    for resultado in lista_resultados:
        nome = resultado.find_element('class name', 'tAxDx').text
        nome = nome.lower()
        #Analisar se tem algum termo banido:
        tem_termos_banidos = False
        for palavra in lista_termos_banidos:
            if palavra in nome:
                tem_termos_banidos = True
        #Analisar se tem todos os termos do nome do produto:
        tem_todas_palavras = True
        for palavra in lista_termos_nome:
            if palavra not in nome:
                tem_todas_palavras = False

        if tem_todas_palavras and not tem_termos_banidos:
            #Preço
            preco = resultado.find_element('class name', 'a8Pemb').text
            preco = preco.replace('R$', '').replace('.', '').replace(' ', '').replace(',','.')
            # Usando regex para encontrar o primeiro número decimal na string
            match = re.search(r'\d+\.\d+', preco)
            # Verifica se houve correspondência e converte para float
            if match:
                preco = float(match.group())
            else:
                continue
            #Link
            elemento_referencia_filho = resultado.find_element('class name', 'bONr3b')
            elemento_pai = elemento_referencia_filho.find_element('xpath', '..')
            link = elemento_pai.get_attribute('href')

            #Verificação final:
            if preco <= preco_maximo and preco >= preco_minimo:
                lista_produtos.append((nome, preco, link))
    return lista_produtos
#lista_produtos_google = buscar_google(navegador, 'iphone 12 64 gb', 'mini watch', 3000, 5000 )

def buscar_buscape(navegador, produto, termos_banidos, preco_minimo, preco_maximo):
    ##BUSCAPÉ:
    #Entrar no buscapé
    link = "https://www.buscape.com.br"
    navegador.get(link)

    #Pesquisar pelo produto
    produto = produto
    produto = produto.lower()
    lista_termos_nome = produto.split(' ')
    termos_banidos = termos_banidos
    termos_banidos = termos_banidos.lower()
    lista_termos_banidos = termos_banidos.split(' ')
    preco_minimo = preco_minimo
    preco_maximo = preco_maximo

    barra_pesquisa = navegador.find_element('xpath', '//*[@id="new-header"]/div[1]/div/div/div[3]/div/div/div[2]/div/div[1]/input')
    barra_pesquisa.send_keys(produto, Keys.ENTER)
    #Pegar as informações do produto
    lista_resultados = navegador.find_elements('class name', 'ProductCard_ProductCard_Inner__gapsh')
    #Para cada resultado -> 1 nome, 1 link e 1 preco
    lista_produtos = []
    for resultado in lista_resultados:
        while len(navegador.find_elements('class name', 'ProductCard_ProductCard_Inner__gapsh')) == 0:
            time.sleep(1)
        nome = resultado.find_element('class name', 'ProductCard_ProductCard_Name__U_mUQ').text
        nome = nome.lower()
        #Analisar se tem algum termo banido:
        tem_termos_banidos = False
        for palavra in lista_termos_banidos:
            if palavra in nome:
                tem_termos_banidos = True
        #Analisar se tem todos os termos do nome do produto:
        tem_todas_palavras = True
        for palavra in lista_termos_nome:
            if palavra not in nome:
                tem_todas_palavras = False

        if tem_todas_palavras and not tem_termos_banidos:
            #Preço
            preco = resultado.find_element('class name', 'Text_MobileHeadingS__HEz7L').text
            preco = preco.replace('R$', '').replace('.', '').replace(' ', '').replace(',','.')
            # Usando regex para encontrar o primeiro número decimal na string
            match = re.search(r'\d+\.\d+', preco)
            # Verifica se houve correspondência e converte para float
            if match:
                preco = float(match.group())
            else:
                continue
            #Link
            link = resultado.get_attribute('href')

            #Verificação final:
            if preco <= preco_maximo and preco >= preco_minimo:
                lista_produtos.append((nome, preco, link))
    return lista_produtos
lista_produtos_buscape = buscar_buscape(navegador, 'iphone 12 64 gb', 'mini watch', 2000, 5000 )
print(lista_produtos_buscape)

#Salvar as ofertas boas em um dataframe

#Exportar pro excel

#Enviar por email o resultado da tabela

# Fecha o navegador
time.sleep(100)
navegador.quit()