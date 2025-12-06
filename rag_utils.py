import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def load_and_split_pdf(file_path):
    """Loads a PDF and splits it into chunks."""
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=400,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

def create_vector_store(chunks, api_key):
    """Creates a FAISS vector store from chunks."""
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def get_retriever(vector_store):
    """Returns a retriever from the vector store."""
    return vector_store.as_retriever()
