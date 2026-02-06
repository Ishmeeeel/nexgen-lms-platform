import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_client() -> Client:
    url = st.secrets["https://taolrdwomfimhlfywjvm.supabase.co"]
    key = st.secrets["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRhb2xyZHdvbWZpbWhsZnl3anZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAzMDAzNjIsImV4cCI6MjA4NTg3NjM2Mn0.5VlOOGIIcLVIjMSk7xledtcqlCZINZ6pz0jKWvJTTjo"]  # publishable/anon key only
    return create_client(url, key)

