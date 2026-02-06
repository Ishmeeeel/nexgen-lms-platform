import streamlit as st
from services.supabase_client import get_client

def track(event_type: str, context: dict | None = None):
    if "user" not in st.session_state:
        return
    supabase = get_client()
    supabase.table("events").insert({
        "user_id": st.session_state["user"]["id"],
        "event_type": event_type,
        "context": context or {}
    }).execute()
