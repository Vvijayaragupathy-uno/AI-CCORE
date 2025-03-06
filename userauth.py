import streamlit as st

ADMIN_PASSWORD = "AICCORE2025"

# Function to check admin access
def is_admin():
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False
    return st.session_state.is_admin

# Sidebar with public and admin access as a menu
def admin_login():
    st.sidebar.header("Navigation Menu")
    menu_selection = st.sidebar.selectbox("Choose Page", ("Public Page", "Admin"))
    if menu_selection == "Admin":
        if not is_admin():
            password = st.sidebar.text_input("Enter Admin Password", type="password")
            if st.sidebar.button("Login"):
                if password == ADMIN_PASSWORD:
                    st.session_state.is_admin = True
                    st.sidebar.success("Logged in as Admin")
                else:
                    st.sidebar.error("Incorrect Password")
        else:
            st.sidebar.success("Logged in as Admin")
    else:
        st.session_state.is_admin = False

# Admin panel
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
    except Exception as e:
        st.error(f"Error: {e}")
