import os
from key import open_ai_key
import streamlit as st
import museum_search
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chat_models import ChatOpenAI

os.environ['OPENAI_API_KEY'] = open_ai_key

tools = [
    Tool(
        func=museum_search.piece_tool,
        name="Piece Search",
        description="útil para encontrar informações sobre uma peça do museu, inserir o nome da peça ou modelo"
    ),
    Tool(
        func=museum_search.type_tool,
        name="Type Search",
        description="útil para encontrar todas as peças do museu de um determinado tipo, inserir apenas o tipo"
    )
]

agent = initialize_agent(tools, ChatOpenAI(temperature=0.5), agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# app framework
st.title('📚🤖 ChatBot do Museu')
prompt = st.text_input('Faça sua pergunta aqui sobre o museu e suas peças:')

if prompt:
    #st.write(agent.run(prompt))
    museum_search.piece_tool(prompt)

else:
    st.write("""
        Selecione a opção de pesquisa, para isto basta digitar:
        
        '0' para informações do museu; \n
        '1 Nome da Peça' para informações específicas sobre alguma peça do arsenal do museu. Ex: '1 Emilia PC'; \n
        '2 Tipo de Peça' para listar todas as peças de determinado tipo. Ex: '2 Computadores'; \n

    """)
