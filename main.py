#Bibliotecas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
#Criação navegador:
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#Importar/Visualizar a base de dados
produtos_df = pd.read_excel('buscas.xlsx')
print(produtos_df)

##GOOGLE:
#Entrar no google
link = "https://www.google.com/webhp?hl=pt-BR&sa=X&ved=0ahUKEwjUn-eMy4mGAxV5LbkGHQFiAgsQPAgJ"
navegador.get(link)
#Pesquisar pelo produto
produto = 'iphone 12 64gb'
barra_pesquisa = navegador.find_element('xpath', '//*[@id="APjFqb"]')
barra_pesquisa.send_keys(produto, Keys.ENTER)
#Entrar na aba shopping

#Pegar as informações do produto


##BUSCAPÉ:


#Salvar as ofertas boas em um dataframe

#Exportar pro excel

#Enviar por email o resultado da tabela

# Fecha o navegador
time.sleep(100)
navegador.quit()