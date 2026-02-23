import streamlit as st
import base64
from io import BytesIO
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import ollama

st.title("Chatbot")
st.caption("A Streamlit chatbot powered by local Ollama")

with st.sidebar:
    ollama_models = ollama.list()
    ollama_models_names = [model['model'] for model in ollama_models['models']]
    model_name = st.selectbox("Model", (ollama_models_names))

def convert_to_base64(file):
    return base64.b64encode(file.getvalue()).decode("utf-8")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Say something or attach an image", accept_file=True, file_type=["png", "jpg", "jpeg"])

if prompt:
    # 1. Append and display user message
    text_content = prompt.text
    img_file = prompt.files[0] if prompt.files else None

    with st.chat_message("user"):
        st.write(text_content)
        if img_file:
            st.image(img_file)

    # 2. Assistant Message logic
    llm = ChatOllama(model=model_name, temperature=0)
    content = [{"type": "text", "text": text_content}]
    if img_file:
        content.append({
            "type": "image_url",
            "image_url": f"data:image/jpeg;base64,{convert_to_base64(img_file)}"
        })
           
    with st.chat_message("assistant"):
        msg = HumanMessage(content=content)
        response = st.write_stream(chunk.content for chunk in llm.stream([msg]))

    # 3. Store the full response in history
    st.session_state.messages.append({"role": "assistant", "content": response})
