import selenium
import pandas as pd
import bs4
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup

# Cria o web driver para o navegador Google Chrome
driver = webdriver.Chrome()

""""
https://www.imdb.com

https://www.imdb.com/search/title/

https://www.imdb.com/search/title/?groups=top_1000

https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc

https://www.imdb.com/search/title/?groups=top_1000&count=100&sort=user_rating,desc

https://www.imdb.com/robots.txt"""

# Conecta na página e extrai o código fonte
driver.get("https://www.imdb.com/search/title/?groups=top_1000&count=100&sort=user_rating,desc")
type(driver)

## Formatando o Código Fonte Extraído com o Parser HTML
#selenium.webdriver.chrome.webdriver.WebDriver
# Formata o código fonte com o parser html
soup = BeautifulSoup(driver.page_source, 'html.parser')
print(soup)
type(soup)
print(soup)
print('apos soup')

# Fecha o navegador usado na extração dos dados
driver.quit()  

## Extraindo os Dados Relevantes da Página Web
# Listas de controle para receber os dados
title = []
years = []
duration = []
ratings = []
vote_count = []
description = []

# Extrai a tag com o título do filme
titulo_filme = soup.find_all('a', attrs = {'class':'ipc-title-link-wrapper'})

# Extrai o texto e armazena os dados na lista
for titulo in titulo_filme:
    nome = titulo.h3.text
    title.append(nome)

# Visualiza os primeiros registros
print(title[0:5])
print("Titulo")

# Tamanho da lista
len(title)

# Extraindo a tag div com outros detalhes do filme
outros_detalhes = soup.findAll('div', attrs = {'class':'sc-b189961a-7 btCcOY dli-title-metadata'})

# Loop para percorrer os detalhes de cada filme
for detalhe in outros_detalhes:
    
    # Encontra o elemento <span> que contém o ano do filme
    year_span = detalhe.span
    
    # Encontra o próximo elemento <span> que contém a duração do filme
    duration_span = year_span.find_next_sibling('span')
    
    # Adiciona o ano do filme à lista de anos
    years.append(year_span.text)
    
    # Adiciona a duração do filme à lista de durações
    duration.append(duration_span.text)

# Visualiza os primeiros registros
years[0:5]
print(years)
# Tamanho da lista
print(len(years))

# Visualiza os primeiros registros
print(duration[0:5])

# Tamanho da lista
print(len(duration))

# Extraindo os dados da tag span com as avaliações dos filmes
avaliacoes = soup.findAll('span', attrs = {'class':'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating'})

# List comprehension para extrair o texto porque tem a estrela também e não vamos utilizar
avaliacoes = [aval.text for aval in avaliacoes]
print("avaliacoes")
print(avaliacoes)

# Loop para percorrer as avaliações de cada filme
for aval in avaliacoes:
    
    # Divide a string da avaliação em duas partes: nota e número de votos
    rating, vote, medida = aval.split('\xa0')
    
    # Adiciona a nota do filme à lista de ratings
    ratings.append(rating)
    
    # Remove os parênteses do número de votos e adiciona à lista de contagem de votos
    vote_count.append(vote.strip('()'))

# Visualiza os primeiros registros
print(ratings[0:5])

# Tamanho da lista
print(len(ratings))

# Visualiza os primeiros registros
print(vote_count[0:5])

# Tamanho da lista
print(len(vote_count))

# Extraindo a tag div com a descrição
des_lst = soup.findAll('div', attrs = {'class':'ipc-html-content-inner-div'})

# List comprehension para extrair o texto
descriptions = [des.text for des in des_lst]

# Visualiza os primeiros registros
print(descriptions[0:5])

# Tamanho da lista
print(len(descriptions))

## Salvando o Resultado do Web Scraping
print(f"Tamanho de 'title': {len(title)}")
print(f"Tamanho de 'description': {len(descriptions)}")
print(f"Tamanho de 'release_year': {len(years)}")
print(f"Tamanho de 'duration': {len(duration)}")
print(f"Tamanho de 'ratings': {len(ratings)}")
print(f"Tamanho de 'votes_count': {len(vote_count)}")

# Prepara o dataframe final
df_movie = pd.DataFrame({'titulo': title, 
                             'descricao': descriptions, 
                             'ano_lancamento': years, 
                             'duracao': duration,
                             'avaliacao': ratings, 
                             'votos': vote_count})

# Shape
print(df_movie.shape)

# Visualiza os primeiros registros
print(df_movie.head())

# Salva o dataframe em CSV
df_movie.to_csv("dataset.csv", index = False)

