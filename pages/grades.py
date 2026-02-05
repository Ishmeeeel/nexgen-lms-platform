import streamlit as st
from services.supabase_client import get_client

if "user" not in st.session_state:
    st.warning("Please sign in.")
    st.stop()

st.header("My Grades")
sb = get_client()
uid = st.session_state["user"]["id"]

rows = sb.table("grades").select("*").eq("user_id", uid).order("graded_at", desc=True).execute().data or []
st.dataframe(rows, use_container_width=True)
