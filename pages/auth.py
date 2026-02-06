
import streamlit as st
from services.supabase_client import get_client

def save_session(res):
    st.session_state["user"] = {
        "id": res.user.id,
        "email": res.user.email,
    }
    st.success("Signed in!")

def login():
    st.subheader("Sign In")
    email = st.text_input("Email")
    pwd = st.text_input("Password", type="password")

    if st.button("Sign In"):
        sb = get_client()
        res = sb.auth.sign_in_with_password({"email": email, "password": pwd})
        if res.user:
            save_session(res)
        else:
            st.error("Invalid credentials")

def signup():
    st.subheader("Create Account")
    email = st.text_input("Email", key="s_email")
    pwd = st.text_input("Password", type="password", key="s_pwd")

    if st.button("Sign Up"):
        sb = get_client()
        sb.auth.sign_up({"email": email, "password": pwd})
        st.info("Account created. Check your email to confirm.")

mode = st.radio("Mode", ["Sign In", "Sign Up"], horizontal=True)

if mode == "Sign In":
    login()
else:
    signup()

if "user" in st.session_state:
    st.success(f"Logged in as {st.session_state['user']['email']}")
    if st.button("Sign Out"):
        get_client().auth.sign_out()
        st.session_state.pop("user", None)
        st.rerun()
