import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

st.title("🦜🔗 Langchain Quickstart App")

with st.sidebar:
    model_name = st.selectbox("Model", ("llama3.2:3b", "qwen3:1.7b", "gemma3:4b", "gemma2:2b", "mistral:latest"))

def generate_response(input_text):
    llm = ChatOllama(model=model_name, temperature=0)
    messages = [HumanMessage(content=input_text)]
    response_placeholder = st.empty()
    full_response = ""
    for chunk in llm.stream(messages):
        full_response += chunk.content
        response_placeholder.info(full_response)

with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)
