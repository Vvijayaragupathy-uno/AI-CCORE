import streamlit as st
from userauth import admin_login, is_admin, admin_panel

# Main app
def main_app():
    st.header("Public App")
    st.write("This is the public-facing part of the app.")

    # Display data to all users
    if "data" in st.session_state:
        st.write("Current Data:")
        st.write(st.session_state.data)
    else:
        st.warning("No data available.")

# Run the app
if __name__ == "__main__":
    admin_login()
    if is_admin():
        admin_panel()
    main_app()
