#Criar um navegador
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
link = "https://www.buscape.com.br"
navegador.get(link)

#Importar/Visualizar a base de dados
produtos_df = pd.read_excel('buscas.xlsx')
print(produtos_df)
#Para cada item dentro da base de dados:
#   - Procurar o produto no google shooping
#       - Verificar se algum dos produtos está dentro da faixa de preços
#   - Procurar o produto no buscapé
#       - Verificar se algum dos produtos está dentro da faixa de preços

#Salvar as ofertas boas em um dataframe

#Exportar pro excel

#Enviar por email o resultado da tabela

# Fecha o navegador
time.sleep(10)
navegador.quit()