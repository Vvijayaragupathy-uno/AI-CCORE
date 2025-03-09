import streamlit as st
from userauth import admin_login, is_admin, admin_panel, admin_login_page
from llm import get_llm_response  # Import the updated get_llm_response function
from visualization import visualization_page

# Main app
def main_app():
    st.header("LLM Response Generator")
    st.write("This app generates responses using a large language model.")

    # User input for the prompt
    prompt = st.text_input("Enter your prompt (e.g., 'What is the capital of France?'):")
    
    # Toggle for streaming
    stream = st.checkbox("Enable streaming", value=True)  # Allow users to toggle streaming
    
    
    
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

if __name__ == "__main__":
    admin_login()
    current_page = st.session_state.get("page", "public")
    if st.session_state.get("show_login_page", False):
        admin_login_page()
    elif current_page == "admin_panel" and is_admin():
        admin_panel()
    elif current_page == "visualization":
        visualization_page()
    else: 
        main_app()
