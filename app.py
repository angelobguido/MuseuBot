import os
from key import open_ai_key
import streamlit as st
import museum_search
from langchain.agents import AgentType, initialize_agent, Tool, Agent
from langchain.chat_models import ChatOpenAI
import langchain.agents.mrkl.base as zero 

os.environ['OPENAI_API_KEY'] = open_ai_key

can_print = False
image_to_print = ''

def print_image(input: str):
    global can_print
    global image_to_print

    res = museum_search.piece(input)
    if len(res) == 0:
        can_print = False
        image_to_print = ''
        return "Não tem imagem"
    
    image_to_print = str(museum_search.df.iloc[res[0]]["Imagens do Objeto"]).replace(";", " ")
    if image_to_print == "":
        can_print = False
        return "Não tem imagem"    

    can_print = True
    
    return "Imagem desenhada"


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
    ),
    Tool(
        func=print_image,
        name="Print Piece",
        description="útil para desenhar uma peça pelo nome dela, pode não desenhar nada"   
    )
]

agent = initialize_agent(tools, ChatOpenAI(temperature=0.5), agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, max_iterations=2, early_stopping_method="generate")

sys_msg = """Você é um assistente do museu do ICMC, deve responder tudo em portugues sobre o que te perguntarem sobre o museu. Não responda nada além do museu e suas peças . Você tem acesso a essas ferramentas:"""

prompt = zero.ZeroShotAgent.create_prompt(prefix=sys_msg, tools=tools)
agent.agent.llm_chain.prompt = prompt

# app framework
st.title('📚🤖 ChatBot do Museu')
prompt = st.text_input('Faça sua pergunta aqui sobre o museu e suas peças:')

if prompt:
    st.write(agent.run(prompt))
    #st.write(museum_search.piece_tool(prompt))

else:
    st.write("""
        Pergunte qualquer coisa para o chat. Ele é capaz de fazer 3 ações: 
        Desenhar uma peça.
        Dizer informações sobre ela.
        Mostrar o nome de todas as peças de um tipo específico.

        OBS: A pergunta pode conter uma composição dessas funções, 
        mas evite fazer consultas longas visto que existe um limite de duas iterações.
    """)

if can_print:
    st.markdown(image_to_print, unsafe_allow_html=True)
