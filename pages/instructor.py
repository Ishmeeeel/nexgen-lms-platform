import streamlit as st
from services.supabase_client import get_client

st.header("Instructor Dashboard")

if "user" not in st.session_state:
    st.warning("Please sign in.")
    st.stop()

sb = get_client()
uid = st.session_state["user"]["id"]

# Courses this teacher teaches
taught = sb.table("instructors")\
    .select("course_id, role, courses(title,description)")\
    .eq("user_id", uid).execute().data or []

if not taught:
    st.info("You are not assigned to any courses as an instructor.")
    st.stop()

course_ids = [t["course_id"] for t in taught]
course_label = {t["course_id"]: t["courses"]["title"] for t in taught}
course_id = st.selectbox("Select a course", course_ids, format_func=lambda c: course_label[c])

st.subheader("Enrolled Students")
enrs = sb.table("enrollments")\
    .select("user_id, status, profiles:profiles(email,full_name)")\
    .eq("course_id", course_id).execute().data or []

st.dataframe([{
    "Student": e["profiles"]["full_name"] or e["profiles"]["email"],
    "Email": e["profiles"]["email"],
    "Status": e["status"],
} for e in enrs], use_container_width=True)

# Submissions
st.subheader("Recent Submissions")
subs = sb.table("submissions")\
    .select("id,submitted_at,assignment_url,note,user_id,profiles:profiles(email,full_name),lessons(title)")\
    .eq("course_id", course_id).order("submitted_at", desc=True).limit(100).execute().data or []

st.dataframe([{
    "When": s["submitted_at"],
    "Student": s["profiles"]["full_name"] or s["profiles"]["email"],
    "Lesson": s["lessons"]["title"] if s.get("lessons") else "",
    "URL": s["assignment_url"],
    "Note": s.get("note",""),
} for s in subs], use_container_width=True)

# Grade entry
st.subheader("Add / Update Grade")
if enrs:
    stu = st.selectbox("Student", [e["user_id"] for e in enrs],
                       format_func=lambda id: next((x["profiles"]["full_name"] or x["profiles"]["email"])
                                                   for x in enrs if x["user_id"] == id))
    item_type = st.selectbox("Type", ["lesson", "quiz", "project"])
    score = st.number_input("Score", min_value=0.0, step=0.5)
    max_score = st.number_input("Max Score", min_value=1.0, step=0.5, value=100.0)

    if st.button("Save Grade"):
        sb.table("grades").insert({
            "user_id": stu,
            "course_id": course_id,
            "item_type": item_type,
            "item_id": None,
            "score": score,
            "max_score": max_score,
        }).execute()
        st.success("Grade saved.")
