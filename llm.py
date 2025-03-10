from typing import Generator, Union, List, Dict
import os
from langchain_groq import ChatGroq  # Use Groq's LangChain integration
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader, CSVLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
import streamlit as st

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MODEL_NAME = "llama3-70b-8192" 

# Initialize Groq client
llm = ChatGroq(temperature=0.7, groq_api_key=GROQ_API_KEY, model_name=MODEL_NAME)

# Function to get LLM response from Groq
def get_llm_response(
    prompt: str,
    max_tokens: int = 500,
    stream: bool = False
):
  
    try:
        if stream:
            # Stream the response
            response = llm.stream(prompt, max_tokens=max_tokens)
            def generate():
                for chunk in response:
                    yield chunk.content  # Extract content from the chunk
            return generate()
        else:
            # Get the full response at once
            response = llm.invoke(prompt, max_tokens=max_tokens)
            return response.content  # Extract content from the response
    except Exception as e:
        return f"Error: {str(e)}"

# RAG Pipeline Setup
def load_and_split_document(file_path: str):
   
    try:
        if file_path.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")  # Specify encoding
        elif file_path.endswith(".csv"):
            loader = CSVLoader(file_path)
        elif file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)  # Use PyPDFLoader for PDF files
        else:
            raise ValueError("Unsupported file type. Only TXT, CSV, and PDF files are supported.")
        
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        return texts
    except Exception as e:
        raise Exception(f"Failed to load document: {str(e)}")

def create_vector_store(texts: List[Dict]):
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(texts, embeddings)
    return vector_store

def setup_rag(vector_store, llm):
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})  # Retrieve top 3 relevant chunks
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,  # Use the provided LLM (Groq)
        chain_type="refine",
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

# Integrate Groq with RAG
def rag_with_groq(qa_chain, prompt: str, max_tokens: int = 500, stream: bool = False):
    
    # Retrieve relevant documents
    result = qa_chain({"query": prompt})
    relevant_docs = result["source_documents"]
    
    # Combine the retrieved documents with the user's prompt
    context = "\n".join([doc.page_content for doc in relevant_docs])
    augmented_prompt = f"Context:\n{context}\n\nQuestion: {prompt}\nAnswer:"
    
    # Get the response from Groq
    response = get_llm_response(augmented_prompt, max_tokens=max_tokens, stream=stream)
    if stream:
        return response, relevant_docs  # Return the generator and relevant docs
    else:
        return response, relevant_docs  # Return the full response and relevant docs
