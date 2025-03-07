# mainapp.py

import streamlit as st
from userauth import admin_login, is_admin, admin_panel, admin_login_page
from llm import get_llm_response

# Main app
def main_app():
    st.header("Public App")
    st.write("This is the public-facing part of the app.")

    # Add LLM integration for direct prompt response
    st.header("LLM-Powered Chat")
    prompt = st.text_input("Enter your prompt (e.g., 'Explain quantum computing in simple terms'):")
    
    if st.button("Get Response"):
        if prompt:
            with st.spinner("Generating response..."):
                # Get response from LLM
                llm_response = get_llm_response(prompt)
                st.write("LLM Response:")
                st.write(llm_response)
        else:
            st.warning("Please enter a prompt to get a response.")

# Run the app
if __name__ == "__main__":
    admin_login()
    
    # Determine which page to show
    current_page = st.session_state.get("page", "public")

    if st.session_state.get("show_login_page", False):
        admin_login_page()
    elif current_page == "admin_panel" and is_admin():
        admin_panel()
    else: 
        main_app()