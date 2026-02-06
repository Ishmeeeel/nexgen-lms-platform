import streamlit as st
from services.supabase_client import get_client

def _save_session(res):
    st.session_state["user"] = {
        "id": res.user.id,
        "email": res.user.email
    }
    st.success("Signed in!")

def show_login():
    st.subheader("Sign in")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign in"):
        supabase = get_client()
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            _save_session(res)
        else:
            st.error("Invalid credentials")

def show_signup():
    st.subheader("Create account")
    email = st.text_input("Email", key="su_email")
    password = st.text_input("Password", type="password", key="su_pwd")
    if st.button("Sign up"):
        supabase = get_client()
        supabase.auth.sign_up({"email": email, "password": password})
        st.info("Account created. Check your email to confirm.")

mode = st.radio("Auth mode", ["Sign in","Sign up"], horizontal=True)
show_login() if mode=="Sign in" else show_signup()

if "user" in st.session_state:
    st.success(f"Logged in as {st.session_state['user']['email']}")
    if st.button("Sign out"):
        get_client().auth.sign_out()
        st.session_state.pop("user", None)
        st.rerun()

