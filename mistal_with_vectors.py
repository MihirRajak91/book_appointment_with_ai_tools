from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
import requests
import numpy as np

MISTRAL_API_URL = "http://127.0.0.1:11434/api/generate"


class DummyEmbeddings(Embeddings):
    """
    A simple embedding generator that creates random embeddings.
    Replace this with a real embedding generator if needed.
    """
    def embed_documents(self, texts):
        return [np.random.rand(512).tolist() for _ in texts]  # Generates random embeddings of size 512

    def embed_query(self, text):
        return np.random.rand(512).tolist()  # Generates random embeddings for a query


def get_pdf_text(pdf):
    """
    Extracts text from a PDF file.
    """
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


def get_text_chunks(text):
    """
    Splits text into manageable chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    chunks = text_splitter.split_text(text)
    return chunks


def create_vector_store(chunks):
    """
    Creates a vector store from text chunks using FAISS.
    Uses DummyEmbeddings for simplicity.
    """
    embeddings = DummyEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store


def query_document(query, vector_store):
    """
    Queries the vector store and Ollama API for a response.
    """
    docs = vector_store.similarity_search(query, k=5)
    relevant_text = " ".join([doc.page_content for doc in docs])

    response = requests.post(
        MISTRAL_API_URL,
        json={
            "model": "mistral",
            "prompt": f"{query}\n{relevant_text}",
            "temperature": 0.3,
            "max_tokens": 1000,
            "stream": False
        }
    )

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("response", "No response")
    else:
        return f"An error occurred: {response.status_code}"
