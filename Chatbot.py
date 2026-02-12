import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

st.title("🦜🔗 Langchain Quickstart App")

def generate_response(input_text):
    llm = ChatOllama(model="gemma2:2b", temperature=0)
    messages = [HumanMessage(content=input_text)]
    st.info(llm.invoke(messages).content)

with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)
