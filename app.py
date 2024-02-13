import langchain
from langchain_google_genai import ChatGoogleGenerativeAI as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings as ge
import streamlit as st
import dotenv
import os
from chat_store import save_conversation, load_conversation
from langchain.chains.conversation.memory import (
    ConversationBufferMemory,
    ConversationSummaryBufferMemory,
    ConversationKGMemory,
    ConversationSummaryMemory
)
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain,ConversationChain
from dotenv import load_dotenv
load_dotenv()
os.environ['GOOGLE_API_KEY']=os.getenv('GOOGLE_API_KEY')

llm=genai(model='gemini-pro')
embeddings=ge(model='models/embeddings-001')
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles.css")  # Load your CSS file

memory = ConversationSummaryBufferMemory(llm=llm)
human_avatar='https://th.bing.com/th/id/R.f307bf56791ab698472f57441c1f14fb?rik=kfAyyfpbDg92hQ&pid=ImgRaw&r=0'
ai_avatar='https://th.bing.com/th/id/R.26802dee07032f0f553419f19490e897?rik=YjFAxIlImCxxrA&pid=ImgRaw&r=0'

st.header('Make Your Assistant')

# Sidebar: Prompt Template 
st.sidebar.header("Prompt Template")
prompt_template = st.sidebar.text_area('Enter your prompt template here:')
apply_button = st.sidebar.button("Apply Template") 

# Main Chat Area
st.header("Conversation")
user_input = st.text_input('Enter your prompt:')
send_button = st.button("Send") 
chat_history = [{"User": "", "Model": ""}]  # Initial placeholder 
template_chain = None

def prompt(prompt_template: str, user_input:str=None):
    # Your updated and excellent prompt function
    if user_input is None:
        user_input=''
    formatted_prompt = f'''
    # Instructions:\n {prompt_template}\n
    # Query: {user_input}
    ''' 
    return PromptTemplate(template=formatted_prompt, input_variables=[user_input]) 

general_chain = LLMChain(
    llm=llm, 
    prompt=prompt("", user_input=user_input), 
    memory=memory, 
    verbose=True
)

# def llm_chain():  
#     memory = ConversationSummaryBufferMemory(llm=llm)
#     chain = ConversationChain(llm=llm, prompt=prompt(prompt_template), memory=memory, verbose=True)
#     return chain


current_history=[]
def handle_input():
    global template_chain
    global current_history

    if send_button or apply_button:
        if not prompt_template and send_button:  # User wants general chat
            output = general_chain.run({'input': user_input})

            # st.write(output)
        elif prompt_template:  # Template case
            if template_chain is None: 
                template_chain = LLMChain(llm=llm,memory=memory, prompt=prompt(prompt_template,user_input=user_input), verbose=True)
            output = template_chain.run({ 'input': user_input})

        # Update Chat History 
        save_conversation([{'User':user_input,'Model':output}])
        
       # Load existing history and display
        current_history = load_conversation()
        print(current_history)
        
        
        # Display Chat History
    for message in current_history:
            if message["User"] and message["Model"]: 
                # Display user message with avatar
                st.markdown(
                    f"<div class='user-message'><img src='{human_avatar}' class='avatar'>{message['User']}</div>",
                    unsafe_allow_html=True
                )
                # Display model message with robot avatar
                st.markdown(
                    f"<div class='model-message'><img src='{ai_avatar}' class='avatar'>{message['Model']}</div>",
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    handle_input()




