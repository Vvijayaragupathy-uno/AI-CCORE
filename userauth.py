from github import Github
import os

def admin_panel():
    st.header("Admin Panel")
    st.write("Welcome, Admin! You can upload new documents (TXT, CSV, or PDF) to the LLM documents folder here.")

    # File uploader
    uploaded_file = st.file_uploader("Upload a new document", type=["txt", "csv", "pdf"])
    
    if uploaded_file is not None:
        # GitHub credentials (use Streamlit secrets)
        GITHUB_TOKEN = st.secrets["API_KEY"]
        REPO_NAME = "Vvijayaragupathy-uno/AI-CCORE"  # Your repository
        LLM_DOCUMENTS_FOLDER = "llm_documents"  # Folder in your repository

        # Initialize GitHub API
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)

        # Read the uploaded file
        file_content = uploaded_file.getvalue()

        # Define the file path in the repository
        file_path = f"{LLM_DOCUMENTS_FOLDER}/{uploaded_file.name}"

        try:
            # Check if the file already exists in the repository
            existing_file = repo.get_contents(file_path)
            # Update the file
            repo.update_file(file_path, f"Update {uploaded_file.name} via Streamlit", file_content, existing_file.sha)
            st.success(f"Document '{uploaded_file.name}' updated successfully in the LLM documents folder on GitHub!")
        except:
            # Create a new file
            repo.create_file(file_path, f"Add {uploaded_file.name} via Streamlit", file_content)
            st.success(f"Document '{uploaded_file.name}' uploaded successfully to the LLM documents folder on GitHub!")

    st.header("Search Assistant")
    st.write("This generates responses using a Deepseek r1 think model.")

    prompt = st.text_input("Prompt to start search")
    
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
