import streamlit as st
from services.supabase_client import get_client

st.header("Admin Panel")

if "user" not in st.session_state:
    st.warning("Sign in first.")
    st.stop()

sb = get_client()
uid = st.session_state["user"]["id"]

me = sb.table("profiles").select("is_admin").eq("id", uid).single().execute().data
if not me or not me["is_admin"]:
    st.error("Admins only.")
    st.stop()

st.subheader("All Submissions")
subs = sb.table("submissions")\
    .select("*, profiles:profiles(email,full_name)")\
    .order("submitted_at", desc=True)\
    .limit(200).execute().data or []

st.dataframe(subs, use_container_width=True)

st.subheader("Activity Events")
events = sb.table("events")\
    .select("*")\
    .order("created_at", desc=True)\
    .limit(200).execute().data or []

st.dataframe(events, use_container_width=True)
