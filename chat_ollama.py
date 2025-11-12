import streamlit as st
from langchain_ollama.llms import OllamaLLM

st.title("Chatbot con Ollama")

llm = OllamaLLM(model="deepseek-v3.1:671b-cloud")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if question := st.chat_input("Pregunta lo que quieras"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Generando respuesta..."):
            response = st.write_stream(llm.stream(question))
        st.session_state.messages.append({"role": "assistant", "content": response})
