import os
from key import open_ai_key
import streamlit as st
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import AnalyzeDocumentChain
from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
import requests
import pandas
import numpy as np
import jellyfish as jf
import math
import re

df = pandas.read_csv("peças.txt")
df = df[["Modelo", "Responsável pela Pesquisa", "Tipo do Objeto", "Descrição do Objeto", "Função/Uso",
         "Ano de Fabricação/Época", "Fabricante", "Local de Fabricação/Origem", "Imagens do Objeto"]]
df = df[df["Modelo"].notna()]
df = df[df["Descrição do Objeto"].notna()]
df.reset_index(inplace=True)

url = "http://143.107.183.188/media/collectiveaccess/images/2/6/78416_ca_attribute_values_value_blob_2655_large.jpg"
response = requests.get(url)

# with open("image.jpg", "wb") as f:
#     f.write(response.content)


# Funcoes

operacao = "tipo"


def pesquisa(entrada: str):
    lst = []
    pesquisa = entrada.split()

    if pesquisa[0] == '0':
        pass

    if pesquisa[0] == '1':
        entrada = entrada[2:]
        lst.extend(pesquisa_peca(entrada))
        pass
    elif pesquisa[0] == '2':
        entrada = entrada[2:]
        lst.extend(pesquisa_tipo(entrada))
        pass

    return lst


def pesquisa_peca(entrada: str):
    res = []
    for index, value in df["Modelo"].items():
        if jf.levenshtein_distance(entrada.lower(), str(value).lower()) <= 0.5 * len(entrada):
            res.append(f"{jf.levenshtein_distance(entrada.lower(), str(value).lower())} {index}")
            pass

    res.sort()
    for i in range(len(res)):
        aux = res[i].split()
        res[i] = int(aux[1])
    global operacao
    operacao = "peca"
    return res


def pesquisa_tipo(entrada: str):
    res = []
    for index, value in df["Tipo do Objeto"].items():
        if jf.levenshtein_distance(entrada.lower(), str(value).lower()) <= 0.4 * len(entrada):
            res.append(index)
            pass
    global operacao
    operacao = "tipo"
    return res


def colhe_informacao(lista, operacao):
    res = []

    if operacao == "peca":
        for indexes in lista:
            res.append([f"Modelo: {df.iloc[indexes]['Modelo']}\n",
                        f"Tipo do Objeto: {df.iloc[indexes]['Tipo do Objeto']}\n",
                        f"Descrição do Objeto: {df.iloc[indexes]['Descrição do Objeto']}\n",
                        f"Ano de Fabricação/Época: {df.iloc[indexes]['Ano de Fabricação/Época']}\n",
                        f"Fabricante: {df.iloc[indexes]['Fabricante']}\n",
                        f"Local de Fabricação/Origem: {df.iloc[indexes]['Local de Fabricação/Origem']}\n"],
                       )
            res.append(f"Imagens do Objeto: {df.iloc[indexes]['Imagens do Objeto']}\n")

    if operacao == "tipo":
        for indexes in lista:
            res.append(f"{df.iloc[indexes]['Modelo']}")

    return res


# app framework
st.title('📚🤖 ChatBot do Museu')
prompt = st.text_input('Faça sua pergunta aqui sobre o museu e suas peças:')

if prompt:
    lista = pesquisa(prompt)
    if operacao == "peca":
        for i in range(len(colhe_informacao(lista, operacao))//2):
            aux = colhe_informacao(lista, operacao)[2*i]
            for item in aux:
                st.write(item)
            st.markdown(colhe_informacao(lista, operacao)[2*i+1], unsafe_allow_html=True)
    else:
        for item in colhe_informacao(lista, operacao):
            st.write(item)

else:
    st.write("""
        Selecione a opção de pesquisa, para isto basta digitar:
        
        '0' para informações do museu; \n
        '1 Nome da Peça' para informações específicas sobre alguma peça do arsenal do museu. Ex: '1 Emilia PC'; \n
        '2 Tipo de Peça' para listar todas as peças de determinado tipo. Ex: '2 Computadores'; \n

    """)
