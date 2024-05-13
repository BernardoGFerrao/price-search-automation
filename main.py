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
    time.sleep(5)
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
lista_produtos_google = buscar_google(navegador, 'iphone 12 64 gb', 'mini watch', 3000, 5000 )
print(lista_produtos_google)
##BUSCAPÉ:


#Salvar as ofertas boas em um dataframe

#Exportar pro excel

#Enviar por email o resultado da tabela

# Fecha o navegador
time.sleep(100)
navegador.quit()