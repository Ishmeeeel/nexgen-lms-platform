import streamlit as st
from services.supabase_client import get_client
from utils.tracking import track

if "user" not in st.session_state:
    st.warning("Please sign in.")
    st.stop()

st.header("My Dashboard")
sb = get_client()
uid = st.session_state["user"]["id"]

# Enrollments + course info
enrs = sb.table("enrollments")\
    .select("course_id, courses(title,description,start_date,end_date)")\
    .eq("user_id", uid).execute().data or []

if not enrs:
    st.info("You are not enrolled in any courses yet.")
else:
    for e in enrs:
        c = e["courses"]
        st.subheader(c["title"])
        st.write(c.get("description",""))
        st.caption(f"{c.get('start_date','?')} → {c.get('end_date','?')}")

track("view_dashboard", {})
