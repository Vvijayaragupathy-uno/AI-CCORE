import streamlit as st
import os
from admin_search import get_llm_response
PASSWORD = st.secrets["PASSWORD"]
ADMIN_PASSWORD = PASSWORD

def is_admin():
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False
    return st.session_state.is_admin

def admin_login():
    st.sidebar.title("AICCORE")
    if not is_admin():
        if st.sidebar.button("Admin"):
            st.session_state.show_login_page = True
            st.rerun()  
    else:
        st.sidebar.success("Logged in as Admin")
        if st.sidebar.button("Logout"):
            st.session_state.is_admin = False
            st.session_state.show_login_page = False
            st.session_state.page = "public"
            st.rerun()  
    if st.sidebar.button("Visualization"):
        st.session_state.page = "visualization"
        st.rerun() 

def admin_login_page():
    st.header("Admin Login")
    st.write("Please enter the admin password to access the admin panel.")
    password = st.text_input("Enter Admin Password", type="password")
    login_col, cancel_col = st.columns([1, 1])
    with login_col:
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.session_state.show_login_page = False
                st.session_state.page = "admin_panel"
                st.rerun() 
            else:
                st.error("Incorrect Password")
    with cancel_col:
        if st.button("Cancel"):
            st.session_state.show_login_page = False
            st.session_state.page = "public"
            st.rerun()  
        

def admin_panel():
    st.header("Admin Panel")
    st.write("Welcome, Admin! You can upload new documents (TXT or CSV or PDF) to the LLM documents folder here.")
    uploaded_file = st.file_uploader("Upload a new document", type=["txt", "csv","pdf"])
    if uploaded_file is not None:
        llm_documents_folder = "llm_documents"
        os.makedirs(llm_documents_folder, exist_ok=True)  
        file_path = os.path.join(llm_documents_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Document '{uploaded_file.name}' uploaded successfully to the LLM documents folder!")

    st.header("Search Assistant")
    st.write("This  generates responses using a Deepseek r1 think model.")

    
    prompt = st.text_input(" prompt to start search")
    
    # Toggle for streaming
    stream = st.checkbox("Enable streaming", value=True) 
    if st.button("Generate Response"):
        if prompt:
            with st.spinner("Generating response..."):
                if stream:
                    # Stream the response incrementally
                    response_container = st.empty()  # Placeholder for the response
                    full_response = ""
                    response_stream = get_llm_response(prompt, stream=True)
                    for chunk in response_stream:
                        full_response += chunk
                        response_container.write(full_response)  # Update the response in real-time
                else:
                    # Generate the full response at once
                    response = get_llm_response(prompt, stream=False)
                    
                    # Extract the thinking process and final answer
                    if "<think>" in response and "</think>" in response:
                        thinking_process = response.split("<think>")[1].split("</think>")[0]
                        final_answer = response.split("</think>")[1].strip()
                    else:
                        thinking_process = None
                        final_answer = response
                    st.write("Final Answer:")
                    st.write(final_answer)
        else:
            st.warning("Please enter a prompt to generate a response.")

    st.header("Web Scraping with ScrapeGraphAI")
    url = st.text_input("Enter the URL to scrape:")
    user_prompt = st.text_input("Enter your prompt (e.g., 'Extract the main heading and description'):")
    ScrapeGraphAI_KEY = st.secrets["ScrapeGraphAI_KEY"]  
    if st.button("Scrape Content"):
        if url and user_prompt:
            with st.spinner("Scraping web content..."):
                try:
                    from scrapegraph_py import Client
                    client = Client(api_key="ScrapeGraphAI_KEY")
                    scraped_data = client.smartscraper(
                        website_url=url,
                        user_prompt=user_prompt
                    )
                    st.session_state.scraped_data = scraped_data
                    st.success("Scraping completed!")
                except Exception as e:
                    st.error(f"Error during scraping: {e}")
        else:
            st.warning("Please enter a valid URL and prompt.")
                 
    if "scraped_data" in st.session_state:
        st.subheader("Scraped Content")
        st.write(st.session_state.scraped_data)
