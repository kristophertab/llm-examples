import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

st.title("🦜🔗 Langchain Quickstart App")

with st.sidebar:
    model_name = st.selectbox("Model", ("llama3.2:3b", "qwen3:1.7b", "gemma3:4b", "gemma2:2b", "mistral:latest"))

st.title("Chatbot")
st.caption("A Streamlit chatbot powered by local Ollama")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # 1. Append and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Assistant Message logic
    llm = ChatOllama(model=model_name, temperature=0)
    with st.chat_message("assistant"):        
        stream = llm.stream(st.session_state.messages)
        response_text = st.write_stream(chunk.content for chunk in stream)

    # 3. Store the full response in history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
