import streamlit as st

ADMIN_PASSWORD = "AICCORE2025"

def is_admin():
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False
    return st.session_state.is_admin

def admin_login():
    st.sidebar.title("Navigation Menu")
    st.sidebar.header("Admin")
    if not is_admin():
        st.sidebar.info("Click on 'Admin' to access the admin login page.")
        if st.sidebar.button("Admin"):
            st.session_state.show_login_page = True
            st.rerun()  # Rerun the app to show the login page
    else:
        st.sidebar.success("Logged in as Admin")
        if st.sidebar.button("Logout"):
            st.session_state.is_admin = False
            st.session_state.show_login_page = False
            st.session_state.page = "public"
            st.rerun()  # Rerun the app to return to the public page
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
                st.rerun()  # Rerun the app to show the admin panel
            else:
                st.error("Incorrect Password")
    with cancel_col:
        if st.button("Cancel"):
            st.session_state.show_login_page = False
            st.session_state.page = "public"
            st.rerun()  # Rerun the app to return to the public page

def admin_panel():
    st.header("Admin Panel")
    st.write("Welcome, Admin! You can update the data here.")

    # Load existing data (e.g., from a CSV file)
    try:
        data = st.session_state.get("data", [])
        if not data:
            st.warning("No data found. Upload a file to start.")
        else:
            st.write("Current Data:")
            st.write(data)

        # Allow admin to upload a new file
        uploaded_file = st.file_uploader("Upload a new CSV file", type=["csv"])
        if uploaded_file is not None:
            import pandas as pd
            new_data = pd.read_csv(uploaded_file)
            st.session_state.data = new_data
            st.success("Data updated successfully!")

        # Add ScrapeGraphAI functionality to the admin panel
        st.header("Web Scraping with ScrapeGraphAI")
        url = st.text_input("Enter the URL to scrape:")
        user_prompt = st.text_input("Enter your prompt (e.g., 'Extract the main heading and description'):")
        
        if st.button("Scrape Content"):
            if url and user_prompt:
                with st.spinner("Scraping web content..."):
                    try:
                        from scrapegraph_py import Client
                        client = Client(api_key="sgai-f313f2c7-73e2-41e8-adcf-9061e01eca53")
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

        # Display scraped data
        if "scraped_data" in st.session_state:
            st.subheader("Scraped Content")
            st.write(st.session_state.scraped_data)

    except Exception as e:
        st.error(f"Error: {e}")
