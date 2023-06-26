import pandas
import requests
import jellyfish as jf

df = pandas.read_csv("peças.txt")
df = df[["Modelo", "Responsável pela Pesquisa", "Tipo do Objeto", "Descrição do Objeto", "Função/Uso",
         "Ano de Fabricação/Época", "Fabricante", "Local de Fabricação/Origem", "Imagens do Objeto"]]
df = df[df["Modelo"].notna()]
df = df[df["Descrição do Objeto"].notna()]
df.reset_index(inplace=True)

#Return museum pieces indexes with names similar to input
def piece(input: str):
    res = []
    for index, value in df["Modelo"].items():
        if jf.levenshtein_distance(input.lower(), str(value).lower()) <= 0.5 * len(input):
            res.append((jf.levenshtein_distance(input.lower(), str(value).lower()), index))

    res.sort()
    res = list(map(lambda x : x[1], res))

    return res

#Return museum pieces indexes with types similar to input
def type(input: str):
    res = []
    for index, value in df["Tipo do Objeto"].items():
        if jf.levenshtein_distance(input.lower(), str(value).lower()) <= 0.5 * len(input):
            res.append(index)

    return res

#Return museum piece information to use as an agent tool
def piece_tool(input: str):
    res = piece(input)

    if (len(res) == 0):
        return ""

    out = f'''
    
    Nome: {df.iloc[res[0]]["Modelo"]}
    Ano de Fabricação/Época: {df.iloc[res[0]]["Ano de Fabricação/Época"]}
    Tipo do Objeto: {df.iloc[res[0]]["Tipo do Objeto"]}
    Descrição: {df.iloc[res[0]]["Descrição do Objeto"]}
    
    Peças com nomes semelhantes: {str([df.iloc[x]["Modelo"] for x in res])}
    
    '''

    return out

#Return museum pieces names according to type
def type_tool(input: str):
    res = type(input)

    if (res.count == 0):
        return ""

    out = f'''
    
    Peças do tipo escolhido: {str([df.iloc[x]["Modelo"] for x in res])}
    
    '''

    return out
