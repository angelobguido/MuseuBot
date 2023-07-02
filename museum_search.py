import pandas
import requests
from thefuzz import process, fuzz
import random
import jellyfish as jf

df = pandas.read_csv("peças.txt")
df = df[["Modelo", "Responsável pela Pesquisa", "Tipo do Objeto", "Descrição do Objeto", "Função/Uso",
         "Ano de Fabricação/Época", "Fabricante", "Local de Fabricação/Origem", "Imagens do Objeto"]]
df = df[df["Modelo"].notna()]
df = df[df["Descrição do Objeto"].notna()]
df.reset_index(inplace=True)

LAST_INFO = ''

#Return indexes based on similarity with attribute value
def take_indexes(input: str, attribute: str):
    res = []

    process.extract(query=input, choices=list(map(lambda x : x[1], df["Modelo"].items())), scorer=fuzz.ratio)

    for index, value in df[attribute].items():
        res.append((fuzz.ratio(input.lower(), str(value).lower()), index))

    res.sort(reverse=True)

    if res[0][0] < 50:
        return []

    res = list(map(lambda x : x[1], res))

    return res

#Return museum piece information to use as an agent tool
def piece_tool(input: str):
    res = take_indexes(input, "Modelo")[:5]

    if (len(res) == 0):
        return ""

    out = f'''
    
    Nome: {df.iloc[res[0]]["Modelo"]}
    Ano de Fabricação/Época: {df.iloc[res[0]]["Ano de Fabricação/Época"]}
    Tipo do Objeto: {df.iloc[res[0]]["Tipo do Objeto"]}
    Descrição: {df.iloc[res[0]]["Descrição do Objeto"]}
    
    Peças com nomes semelhantes: {str([df.iloc[x]["Modelo"] for x in res])}
    
    '''

    global LAST_INFO
    LAST_INFO = out
    return out

#Return museum pieces names according to type
def type_tool(input: str):
    res = take_indexes(input, "Tipo do Objeto")

    if (res.count == 0):
        return ""

    out = f'''
    
    Peças do tipo escolhido: {str([df.iloc[x]["Modelo"] for x in res])}
    
    '''

    global LAST_INFO
    LAST_INFO = out
    return out

#Return museum info
def museum_info_tool(input: str):
    
    out = f'''

    O Museu de Computação do ICMC teve origem como um Museu de Instrumentos de Cálculo Numérico idealizado pelo Prof. Odelar Leite Linhares. 
    Com o surgimento das minicalculadoras digitais, os antigos instrumentos de cálculo tornaram-se obsoletos, levando à criação do museu. 
    O acervo recebeu doações de peças e foi instalado na Biblioteca Prof. Achile Bassi. Após a aposentadoria do Prof. Odelar, o museu ficou 
    sob a coordenação do Departamento de Ciências de Computação e Estatística. O acervo continuou a crescer com doações de computadores e 
    dispositivos obsoletos. O espaço do museu foi ampliado em 2013 e 2014, visando integrá-lo ao ambiente acadêmico. O novo espaço foi 
    inaugurado em junho de 2014 com a exposição "Computação e Copa em um só ritmo". 
    
    Mais informações estão disponíveis no site do museu: https://mc.icmc.usp.br/exposi%C3%A7%C3%B5es.
    
    '''

    global LAST_INFO
    LAST_INFO = out
    return out

#Return assistent info
def assistant_info_tool(input: str):
    
    out = f'''
    
    Você é um assistente de museu do ICMC. Você é capaz de realizar diversas operações sobre as peças do museu e sobre o museu em si.
    Algumas de suas utilidades são:
    
    Falar sobre o museu do ICMC. 
    Desenhar uma peça.
    Dizer informações sobre uma peça.
    Dizer nomes de peças próximos a um nome de peça.
    Mostrar o nome de todas as peças de um tipo específico.
    Pegar o nome de algumas peças do museu de exemplo.

    OBS: A pergunta pode conter uma composição dessas funções, 
    mas evite fazer consultas longas visto que existe um limite de iterações.

    '''

    return out

#Return random example pieces
def example_tool(input: str):

    pieces = list(map( lambda x: x[1], random.sample(list(df["Modelo"].items()), 5)))

    return str(pieces)