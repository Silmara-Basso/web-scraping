import PIL
import random
import wordcloud
import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.express as px
from wordcloud import WordCloud
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# Carrega o dataset
df_filmes = pd.read_csv('dataset.csv')
# Shape
df_filmes.shape
print(df_filmes.info())
# Primeiros registros
print(df_filmes.head())

## Limpeza dos Dados Para Análise
# Visualiza primeiras linhas de uma das colunas
df_filmes['titulo'].head()
# Divide a string da coluna 'titulo' em duas partes, separando pelo primeiro espaço
novo = df_filmes['titulo'].str.split(" ", n = 1, expand = True)
# Visualiza primeiras linhas
print(novo.head())

# Adiciona o título extraído de volta ao dataframe
df_filmes['titulo'] = novo[1]
# Visualiza primeiras linhas
print(df_filmes['titulo'].head())

# Nomes das colunas
df_filmes.columns
# Visualiza primeiras linhas
print(df_filmes['duracao'].head())

# Função para converter o tempo no formato 'xh ym' para minutos
def converte_hora(time):
    
    # Divide a string 'time' em uma lista de partes, separadas por espaços
    time = time.split(' ')
    
    # Extrai a parte da hora (antes do 'h') e converte para um número inteiro
    hour = int(time[0].split('h')[0].strip())
    
    # Verifica se existe uma parte de minutos na lista de tempo
    if len(time) == 2:
        
        # Extrai a parte dos minutos (antes do 'm') e converte para um número inteiro
        minute = int(time[1].split('m')[0].strip())
        
        # Retorna o tempo total em minutos (hora em minutos + minutos)
        return hour * 60 + minute
    
    else:
        
        # Se não houver minutos, retorna apenas o tempo em horas convertido para minutos
        return hour * 60
    
# Aplica a função
df_filmes['duracao'] = df_filmes['duracao'].apply(converte_hora)
# Visualiza primeiras linhas
print(df_filmes['duracao'].head())
# Nomes das colunas
print(df_filmes.columns)
# Visualiza primeiras linhas
print(df_filmes['votos'].head())


# Função para converter a unidade dos votos de milhões (M) ou milhares (K) para um número em milhares
def converte_unidade(votes):
    
    # Verifica se o número de votos contém a letra 'M' (milhões)
    if 'M' in votes:
        
        # Remove a letra 'M', converte para float e multiplica por 1000 para obter o valor em milhares
        return float(votes.replace('M', '')) * 1000
    
    else:
        
        # Caso contrário, remove a letra 'K' (milhares) e converte diretamente para float
        return float(votes.replace('K', '') and votes.replace(',', '.'))

# Aplica a função
df_filmes['votos(K)'] = df_filmes['votos'].apply(converte_unidade)
# Não precisamos mais da coluna original
df_filmes.drop(columns = ['votos'], inplace = True)
# Visualiza primeiras linhas
print(df_filmes.head())

# Verifica se há valores ausentes
print(df_filmes.isna().sum())

# Verifica se há linhas duplicadas
print(df_filmes.duplicated().sum())

# Visualiza primeiras linhas
print(df_filmes.head())

### 1- Quantos Filmes Foram Lançados a Cada Ano?
# Contagem de filmes por ano
filmes_por_ano = df_filmes['ano_lancamento'].value_counts().sort_index()
# Cria um DataFrame auxiliar
df_filmes_por_ano = filmes_por_ano.reset_index()
df_filmes_por_ano.columns = ['Ano', 'Número de Filmes']
# Gráfico interativo
fig = px.bar(df_filmes_por_ano, x = 'Ano', y = 'Número de Filmes', title = 'Número de Filmes Lançados Por Ano')
fig.update_layout(xaxis_tickangle = -45)
fig.show()

### 2- Qual Década Teve o Maior Número de Lançamentos de Filmes?

# Visualiza primeiras linhas
print(df_filmes.head())
# Crie nova coluna com range de décadas
df_filmes['decada_lancamento'] = df_filmes['ano_lancamento'] // 10 * 10
# Visualiza primeiras linhas
print(df_filmes.head())

# Plot

# Definindo o estilo darkgrid
sns.set_style("darkgrid")

# Tamanho da figura
plt.figure(figsize = (12, 6))

# Barplot
ax = sns.barplot(x = 'decada_lancamento', 
                 y = 'avaliacao', 
                 data = df_filmes, 
                 palette = 'pastel', 
                 estimator = lambda x: len(x))

# Adicionar anotações nas barras
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{int(height)}', 
                (p.get_x() + p.get_width() / 2., height), 
                ha = 'center', 
                va = 'center', 
                xytext = (0, 9), 
                textcoords = 'offset points')

# Títulos e rótulos
plt.title('Número de Filmes Por Década\n')
plt.xlabel('\nDécada de Lançamento')
plt.ylabel('Número de Filmes')
plt.show()

### 3- Demonstre com Gráfico de Bolhas a Relação Entre Avaliação e Duração, Com Número de Votos.
# Plot
plt.figure(figsize = (12, 6))
plt.scatter(df_filmes['duracao'], 
            df_filmes['avaliacao'], 
            s = df_filmes['votos(K)'], 
            alpha = 0.5, 
            c = df_filmes['votos(K)'], 
            cmap = 'viridis')
plt.title('Relação Entre Avaliação e Duração, Com Número de Votos\n')
plt.xlabel('\nDuração (min)')
plt.ylabel('Avaliação')
plt.show()

""""
O parâmetro s define o tamanho de cada ponto no gráfico de dispersão. Em nosso caso estamos definindo o tamanho dos pontos de acordo com os valores na coluna df_filmes['votos(K)']. Isso significa que o tamanho de cada ponto será proporcional ao número de votos que cada filme (ou outra unidade de observação) recebeu. Em outras palavras, filmes com mais votos terão pontos maiores e filmes com menos votos terão pontos menores.

O parâmetro alpha controla a transparência dos pontos no gráfico. O valor pode variar de 0 a 1:

- alpha=1 significa que os pontos serão completamente opacos.
- alpha=0.5 significa que os pontos terão 50% de opacidade, ou seja, serão parcialmente transparentes.
- alpha=0 deixaria os pontos completamente invisíveis.

Um colormap é uma paleta de cores que mapeia valores numéricos para cores específicas. Em nosso caso, o parâmetro c define quais valores serão usados para colorir os pontos e o colormap (cmap) determina como essas cores são escolhidas com base nesses valores.
"""

### 4- Qual a Força da Correlação Entre Duração do Filme e o Número de Votos? 
# Plot
plt.figure(figsize = (12, 6))
sns.scatterplot(data = df_filmes, x = 'duracao', y = 'votos(K)', c = 'purple')
plt.title('Correlação Entre Duração do Filme e Número de Votos')
plt.xlabel('\nDuração')
plt.ylabel('Número de Votos')
plt.show()

# Cálculo do coeficiente de correlação entre as variáveis 'duracao' e 'votos(K)'
correlacao = df_filmes['duracao'].corr(df_filmes['votos(K)'])
# Exibe o valor da correlação
print(f'Coeficiente de Correlação entre Duração e Número de Votos: {correlacao}')

""""
O coeficiente de correlação mede a força e a direção de uma relação linear entre duas variáveis. Ele resulta em um valor numérico entre -1 e 1:

- 1: Indica uma correlação perfeita positiva, ou seja, à medida que uma variável aumenta, a outra também aumenta de forma proporcional.
- 0: Indica nenhuma correlação linear, ou seja, as variáveis não têm uma relação linear direta.
- -1: Indica uma correlação perfeita negativa, ou seja, à medida que uma variável aumenta, a outra diminui de forma proporcional.
"""

### 5- Crie Uma Nuvem de Palavras Mostrando as Palavras Mais Frequentes na Descrição dos Filmes.
# Visualiza primeiras linhas
print(df_filmes.head())
# Une os textos de todas as descrições
texto = ' '.join(df_filmes['descricao'])
print(texto)

# Usamos uma imagem como máscara para desenha a word cloud
mascara = np.array(Image.open("stormtrooper_mask.png"))

# Referência: https://github.com/amueller/word_cloud
# Cria a nuvem de palavras
wc = WordCloud(max_words = 1000, mask = mascara, margin = 8, random_state = 1).generate(texto)
# Plot
plt.figure(figsize = (14, 8))
array_imagem = wc.to_array()
plt.title("Word Cloud Para Descrição dos Filmes\n")
plt.imshow(array_imagem, interpolation = "bilinear")
plt.axis("off")
plt.show()

# Salva em disco
wc.to_file("a_new_hope.png")

# Se quiser algo mais tradicional...
# Cria a nuvem de palavras
wordcloud = WordCloud(width = 800, height = 400, background_color = 'white').generate(texto)
# Plot da nuvem de palavras
plt.figure(figsize = (12, 6))
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')
plt.title('Word Cloud Para Descrição dos Filmes\n')
plt.show()

# Salva em disco
wordcloud.to_file("wordcloud.png")