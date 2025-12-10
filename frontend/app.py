import streamlit as st 
import requests
import os 
from dotenv import load_dotenv

load_dotenv()

# url = "http://127.0.0.1:8000/rag/query"

# This use when frontend are deployed


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
        
        response = requests.post(BACKEND_URL, json={"prompt": prompt,
                                "history": st.session_state.messages})
        
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

if __name__=="__main__":
    
    init_message_state()
    layout()