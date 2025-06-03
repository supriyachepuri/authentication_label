import os
from supabase import create_client
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if SUPABASE_URL and SUPABASE_KEY:
    client = create_client(SUPABASE_URL, SUPABASE_KEY, http_client=None)
else:
    st.error("Supabase credentials not found in .env file")
    st.stop()

# Check session state
if 'user' in st.session_state:
    # User is logged in
    st.write(f"Welcome, {st.session_state.user.email}!")
    if st.button("Logout"):
        st.session_state.user = None
    st.stop()
else:
    # Authentication form
    st.title("Authentication App")
    view = st.radio("Choose an option", ('Login', 'Register'))

    if view == 'Login':
        # Login form
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.markdown("### Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                try:
                    user_data = client.auth.login(email=email, password=password)
                    st.session_state.user = user_data.user
                    st.success("You have successfully logged in!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(str(e))
    elif view == 'Register':
        # Registration form
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.markdown("### Register")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            username = st.text_input("Username")
            if st.button("Register"):
                try:
                    # Create user account
                    user = client.auth.create_user(email=email, password=password, user_info={'username': username})
                    
                    # Save registration details to 'login_details' table
                    data = client.from_('login_details').insert([
                        {'Email': email, 'Username': username, 'created_at': 'now()', 'Password':password}
                    ])
                    st.success("You have successfully registered! Please login.")
                except Exception as e:
                    st.error(str(e))

    # Password reset
    if st.button("Forgot Password?"):
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            email = st.text_input("Email")
            if st.button("Reset Password"):
                try:
                    client.auth.reset_password_email(email=email)
                    st.success("Password reset link sent to your email!")
                except Exception as e:
                    st.error(str(e))