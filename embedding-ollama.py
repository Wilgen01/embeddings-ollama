import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from tempfile import NamedTemporaryFile


prompt_template = """
    Eres un asistente experto en preguntas y respuestas (Q&A) especializado en documentos.
    Tu única fuente de información son los fragmentos de contexto que se te proporcionan.
    Si la respuesta no se encuentra en ese contexto, debes responder simplemente que no lo sabes.
    Tu respuesta debe ser concisa y directa, basándote únicamente en el contexto dado.

    Contexto: {context}
    Pregunta del usuario: {input}
"""

st.set_page_config(page_title="Chat Pdf", layout="wide")
st.title("Chatbot con un PDF - powered by ollama")
uploaded_file = st.sidebar.file_uploader(
    "Sube tu PDF aquí",
    type="pdf"
)

embeddings = OllamaEmbeddings(model="qwen3-embedding:4b")
llm = OllamaLLM(model="gpt-oss:120b-cloud")


def load_file(uploaded_file):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name

    loader = PyPDFLoader(temp_file_path)    
    return loader.load()

def split_document(document):
    text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", ".", "!", "?", " ", ""],
                add_start_index=True
            )
    return text_splitter.split_documents(document)

def create_embeddings_from_file(uploaded_file):
    documents = load_file(uploaded_file)
    document_chunk = split_document(documents)
    vectorstore = InMemoryVectorStore.from_documents(
            documents=document_chunk,
            embedding=embeddings
        )
    
    return vectorstore.as_retriever()

def answer_question(retriever, user_prompt):
    retrieved_documents = retriever.invoke(user_prompt)
    context = "\n\n".join([doc.page_content for doc in retrieved_documents])
    final_prompt = ChatPromptTemplate.from_template(template=prompt_template)
    chain = final_prompt | llm

    st.write("🧠 **Contexto enviado al modelo:**")
    st.write(context)

    st.write("💬 **Pregunta del usuario:**")
    st.write(user_prompt)

    st.write("🧩 **Prompt final construido:**")
    st.write(final_prompt.format(context=context, input=user_prompt))
    return chain.invoke({"context": context, "input": user_prompt})

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if uploaded_file:
    if "file_processed" not in st.session_state or st.session_state.file_processed != uploaded_file.name:
        st.session_state.retriever = create_embeddings_from_file(uploaded_file)
        st.session_state.messages.append({
            "role": "ai",
            "content": "PDF listo. ¿En qué puedo ayudarte con este documento?"
        })
        st.chat_message("ai").write("PDF listo. ¿En qué puedo ayudarte con este documento?")
        st.session_state.file_processed = uploaded_file.name
        
    retriever = st.session_state.retriever

    if question := st.chat_input("Pregunta lo que quieras"):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("analizando tu documento..."):
                response = answer_question(retriever, question)
            message_placeholder.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})






