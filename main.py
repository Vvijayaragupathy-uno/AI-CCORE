import streamlit as st
import os
from llm import load_and_split_document, create_vector_store, rag_with_groq, setup_rag
from langchain_groq import ChatGroq 
from visualization import visualization_page


GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MODEL_NAME = "llama3-70b-8192" 

def load_documents_from_folder(folder_path: str):
    texts = []
    if not os.path.exists(folder_path):
        raise Exception(f"Folder not found: {folder_path}")
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(".txt") or file_name.endswith(".csv") or file_name.endswith(".pdf"):
            try:
                print(f"Loading document: {file_path}")
                texts.extend(load_and_split_document(file_path))
            except Exception as e:
                raise Exception(f"Failed to load {file_name}: {str(e)}")
    
    if not texts:
        raise Exception("No valid documents found in the folder.")
    
    return texts

def main_app():
    st.header("Explore more about LLM Benchmark")
    st.write("data are preloaded by admin")

    llm_documents_folder = "llm_documents"
    try:
        texts = load_documents_from_folder(llm_documents_folder)
        vector_store = create_vector_store(texts)
    except Exception as e:
        st.error(f"Failed to load documents: {str(e)}")
        st.warning("Please ask the admin to upload documents to the 'llm_documents' folder.")
        return

    # Initialize Groq LLM
    llm = ChatGroq(temperature=0.7, groq_api_key=GROQ_API_KEY, model_name=MODEL_NAME)
    
    # Set up RAG pipeline
    qa_chain = setup_rag(vector_store, llm)

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    st.write("### AICCORE Assistant ")
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input for the prompt
    prompt = st.chat_input("ask more about best model or low cost  model")
    
    # Toggle for streaming
    stream = st.checkbox("Enable streaming", value=True) 
    
    if prompt:
       
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        
        with st.chat_message("assistant"):
            if stream:
                
                response_container = st.empty()  
                full_response = ""
                response_stream, relevant_docs = rag_with_groq(qa_chain, prompt, stream=True)
                for chunk in response_stream:
                    full_response += chunk
                    response_container.write(full_response)  
                
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            else:
                
                response, relevant_docs = rag_with_groq(qa_chain, prompt, stream=False)
                st.write("Final Answer:")
                st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Display relevant documents
           # st.write("### Relevant Documents")
           # for doc in relevant_docs:
               # st.write(doc.page_content)
