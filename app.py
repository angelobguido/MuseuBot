import os
import prompt_museum
from key import open_ai_key
import streamlit as st
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import AnalyzeDocumentChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain

from langchain.document_loaders import TextLoader, PDFMinerLoader, CSVLoader

loaders = [TextLoader("teste.txt"), CSVLoader("peças.txt")]
documents = []
for loader in loaders:
    documents.extend(loader.load())


os.environ['OPENAI_API_KEY'] = open_ai_key


text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings, persist_directory='db')
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), vectorstore.as_retriever(), memory=memory, qa_prompt=prompt_museum.QA_PROMPT)

# app framework
st.title('📚🤖 ChatBot do Museu')
prompt = st.text_input('Faça sua pergunta aqui sobre o museu e suas peças:')

if prompt:
    response = qa({"question": prompt})
    st.write(response["answer"])