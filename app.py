import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from tempfile import NamedTemporaryFile
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate



prompt_template = """
Eres un asistente experto en preguntas y respuestas (Q&A) especializado en documentos.
Tu única fuente de información son los fragmentos de contexto que se te proporcionan.
Si la respuesta no se encuentra en ese contexto, debes responder simplemente que no lo sabes.
Tu respuesta debe ser concisa y directa, basándote únicamente en el contexto dado.

Contexto: {context}
Pregunta del usuario: {input}
"""

st.set_page_config(page_title="Chat Pdf", layout="wide")
st.title("Chatea con un PDF");

uploaded_file = st.sidebar.file_uploader(
    "Sube tu PDF aquí",
    type="pdf"
)

path = "pdfs/"

os.makedirs(path, exist_ok=True)

def process_pdf(uploaded_file):
        
        try:
            # with open(f"pdfs/{uploaded_file.name}", "wb") as file:
            #      file.write(uploaded_file.getbuffer())
            with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_path = temp_file.name

            loader = PyPDFLoader(temp_file_path)    
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", ".", "!", "?", " ", ""]
            )

            chunks = text_splitter.split_documents(documents)

            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings
            )

            st.sidebar.success(f"PDF procesado. Chunks generados: {len(chunks)}")

            return vector_store
        finally:
            if 'tmp_file_path' in locals() and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

def get_ollama_model(model_name: str = "phi3:mini"):
    """Inicializa la conexión con el modelo de Ollama."""

    return ChatOllama(
        model=model_name,
        base_url="http://localhost:11434" 
    )


llm = get_ollama_model()

# def get_rag_chain():
#     llm = get_ollama_model()

#     document_chain = create_stuff_documents_chain(llm, RAG_PROMPT)

#     return document_chain

if uploaded_file:
    vector_store = process_pdf(uploaded_file)
    st.session_state["vector_store"] = vector_store

    st.write(f"archivo cargado **{uploaded_file.name}**")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "PDF listo. ¿En qué puedo ayudarte con este documento?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

else:
    st.info("Por favor, sube un archivo PDF para comenzar.")


# rag_chain_structure = get_rag_chain()


def retrieve_context(user_prompt, vector_store):
    return vector_store.similarity_search(user_prompt)

def answer_question(user_prompt, doc_context):
    context = "\n\n".join([doc.page_content for doc in doc_context])
    final_prompt = ChatPromptTemplate.from_template(template=prompt_template)
    chain = final_prompt | llm

    return chain.invoke({"context": context, "input": user_prompt})


if user_prompt := st.chat_input("Escribe tu pregunta sobre el PDF..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)

    if "vector_store" not in st.session_state:
        st.error("Por favor, sube y procesa un PDF primero.")
        st.stop()

    doc_context = retrieve_context(user_prompt, st.session_state.vector_store)

    answer = answer_question(user_prompt=user_prompt, doc_context=doc_context)

    st.chat_message("assistant").write(answer)
