import streamlit as st 
import requests
import os 
from dotenv import load_dotenv

load_dotenv()

# url = f"https://rg-chatbot-de24.azurewebsites.net/rag/query?code={os.getenv('FUNCTION_APP_API')}"

BACKEND_URL = os.getenv("BACKEND_URL")



def init_message_state():
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
def display_chat_message():
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
def handle_user_messager():
    if prompt := st.chat_input("Answer question about Data Engineer"):
        with st.chat_message("user"):
            st.markdown(prompt)
            
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        response = requests.post(BACKEND_URL, json={"prompt": prompt})
        
        data = response.json()
        
        assistant_answer = data["answer"]
        
        with st.chat_message("assistant"):
            st.markdown(assistant_answer)
            
        st.session_state.messages.append({"role": "assistant", "content": assistant_answer})


def layout():
    st.markdown("# Data Engineer chatbot")
    st.markdown("Ask your question.")
    
    display_chat_message()
    handle_user_messager()

    if not BACKEND_URL:
        st.write("BACKEND_URL: är inte satt i miljön")
        raise RuntimeError("BACKEND_URL sakans - Kolla Appsettings i Azure")
if __name__=="__main__":
    
    init_message_state()
    layout()