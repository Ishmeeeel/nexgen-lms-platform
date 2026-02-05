import streamlit as st
from supabase import create_client, Client

# 1. Setup the Page
st.set_page_config(page_title="LMS Platform", page_icon="🎓")

# 2. Connect to Supabase
# We get the keys from the secrets file you just made
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)

# 3. Session State (Memory)
# This remembers if the user is logged in
if 'user' not in st.session_state:
    st.session_state.user = None

# --- FUNCTIONS ---
def login_user(email, password):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user = response.user
        st.success("Login successful!")
        st.rerun() # Refresh the page to show the dashboard
    except Exception as e:
        st.error(f"Error: {e}")

def signup_user(email, password):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        st.success("Account created! Check your email to confirm, or try logging in if auto-confirm is on.")
    except Exception as e:
        st.error(f"Error: {e}")

def logout_user():
    supabase.auth.sign_out()
    st.session_state.user = None
    st.rerun()

# --- THE APP FLOW ---

# A. IF NOT LOGGED IN -> SHOW LOGIN SCREEN
if not st.session_state.user:
    st.title("🎓 Welcome to the LMS")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log In"):
            login_user(email, password)
            
    with tab2:
        st.write("New Student? Register here.")
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            signup_user(new_email, new_password)

# B. IF LOGGED IN -> SHOW THE DASHBOARD
else:
    user_email = st.session_state.user.email
    st.sidebar.write(f"Logged in as: **{user_email}**")
    
    if st.sidebar.button("Log Out"):
        logout_user()
    
    st.title("🚧 Main Dashboard")
    st.write("You are inside! This is where we will put the assignment upload button next.")