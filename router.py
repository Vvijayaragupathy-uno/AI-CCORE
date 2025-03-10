import streamlit as st
from userauth import admin_login, is_admin, admin_login_page
from visualization import visualization_page
from article import article_page
from main import main_app

def router():
    
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"  
    if "show_login_page" not in st.session_state:
        st.session_state.show_login_page = False

    # Sidebar navigation
    st.sidebar.title("AICCORE 2025")
    if st.sidebar.button("Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.sidebar.button("Articles"):
        st.session_state.page = "articles"
        st.rerun()

    if st.sidebar.button(" AI Assistant"):
        st.session_state.page = "AI Assistant"
        st.rerun()

    if not is_admin():
        if st.sidebar.button("Admin Login"):
            st.session_state.show_login_page = True
            st.session_state.page = "admin_login"
            st.rerun()
    else:
        st.sidebar.success("Logged in as Admin")
        if st.sidebar.button("Logout"):
            st.session_state.is_admin = False
            st.session_state.show_login_page = False
            st.session_state.page = "Dashboard"
            st.rerun()

    
    if st.session_state.show_login_page:
        admin_login_page()
    elif st.session_state.page == "admin_panel" and is_admin():
        admin_panel()
    elif st.session_state.page == "articles":
        article_page()
    elif st.session_state.page == "Dashboard":
        visualization_page()
    else:
        main_app() 
