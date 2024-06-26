#Bibliotecas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time
import re

#Criação navegador:
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
def enviar_email():
    # Criar o corpo do email
    corpo_email = f"""
    <p>Prezado,</p>
    <p>Encontramos alguns produtos em oferta dentro da faixa de preço desejada</p>
    {tabela_ofertas.to_html(index=False)}
    <p>Att., Bernardo </p>
    """

    # Configurar a mensagem do email
    msg = MIMEMultipart()
    msg['Subject'] = f"Produto(s) encontrado(s) na faixa de preço desejada"
    msg['From'] = 'seuemail@gmail.com'  # Coloque seu email aqui
    msg['To'] = 'seuemail@gmail.com'

    # Adicionar o corpo do email
    msg.attach(MIMEText(corpo_email, 'html'))

    # Configurações de segurança
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    password = 'suasenhadeapp'  # Coloque sua senha aqui
    s.login(msg['From'], password)

    # Enviar o email
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    print('Email enviado')
def verificar_termos_banidos(lista_termos_banidos, nome):
    # Analisar se tem algum termo banido:
    tem_termos_banidos = False
    for palavra in lista_termos_banidos:
        if palavra in nome:
            tem_termos_banidos = True
    return tem_termos_banidos
def verificar_termos_nome(lista_termos_nome, nome):
    # Analisar se tem todos os termos do nome do produto:
    tem_todas_palavras = True
    for palavra in lista_termos_nome:
        if palavra not in nome:
            tem_todas_palavras = False
    return tem_todas_palavras
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
    while len(navegador.find_elements('xpath', '//*[@id="hdtb-sc"]/div/div/div[1]/div/div[2]/a')) == 0:
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
        tem_termos_banidos = verificar_termos_banidos(lista_termos_banidos, nome)
        #Analisar se tem todos os termos do nome do produto:
        tem_todas_palavras = verificar_termos_nome(lista_termos_nome, nome)

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

        # Analisar se tem algum termo banido:
        tem_termos_banidos = verificar_termos_banidos(lista_termos_banidos, nome)
        # Analisar se tem todos os termos do nome do produto:
        tem_todas_palavras = verificar_termos_nome(lista_termos_nome, nome)

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

#Importar/Visualizar a base de dados
produtos_df = pd.read_excel('buscas.xlsx')

tabela_ofertas = pd.DataFrame()
# Iterando pelas linhas do produtos_df usando .index
for linha in produtos_df.index:
    produto = produtos_df.loc[linha, 'Nome']
    termos_banidos = produtos_df.loc[linha, 'Termos banidos']
    preco_minimo = produtos_df.loc[linha, 'Preço mínimo']
    preco_maximo = produtos_df.loc[linha, 'Preço máximo']

    lista_google_shopping = buscar_google(navegador, produto, termos_banidos, preco_minimo, preco_maximo)
    lista_buscape = buscar_buscape(navegador, produto, termos_banidos, preco_minimo, preco_maximo)

    #Combinar os resultados:
    if lista_google_shopping:
        tabela_google_shopping = pd.DataFrame(lista_google_shopping, columns=['produto', 'preco', 'link'])
        tabela_ofertas = pd.concat([tabela_ofertas, tabela_google_shopping])
    else:
        tabela_google_shopping = None
    if lista_buscape:
        tabela_buscape = pd.DataFrame(lista_buscape, columns=['produto', 'preco', 'link'])
        tabela_ofertas = pd.concat([tabela_ofertas, tabela_buscape])
    else:
        tabela_buscape = None

#Exportar pro excel
tabela_ofertas.to_excel('ofertas.xlsx', index=False)

#Enviar por email o resultado da tabela
enviar_email()

# Fecha o navegador
navegador.quit()