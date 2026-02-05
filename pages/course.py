import streamlit as st
from services.supabase_client import get_client
from utils.tracking import track

if "user" not in st.session_state:
    st.warning("Please sign in.")
    st.stop()

st.header("My Courses & Assignments")
sb = get_client()
uid = st.session_state["user"]["id"]

# Student's courses
enrs = sb.table("enrollments").select("course_id,courses(title)").eq("user_id", uid).execute().data or []
if not enrs:
    st.info("No enrolled courses.")
    st.stop()

course_map = {e["course_id"]: e["courses"]["title"] for e in enrs}
course_id = st.selectbox("Select Course", list(course_map.keys()), format_func=lambda c: course_map[c])

# Lessons
lessons = sb.table("lessons").select("*").eq("course_id", course_id).order("order_index").execute().data or []
st.subheader("Lessons")
for l in lessons:
    st.write(f"- **{l['title']}** — {l.get('scheduled_at','')}")

track("view_course", {"course_id": course_id})

# Assignment submission
st.divider()
st.subheader("Submit Assignment URL")

lesson_id = st.selectbox(
    "Lesson",
    [l["id"] for l in lessons],
    format_func=lambda i: next(x["title"] for x in lessons if x["id"] == i),
)

url = st.text_input("Paste assignment URL (GitHub, Colab, etc.)")
note = st.text_area("Notes (optional)")

if st.button("Submit"):
    sb.table("submissions").insert({
        "user_id": uid,
        "course_id": course_id,
        "lesson_id": lesson_id,
        "assignment_url": url,
        "note": note,
    }).execute()
    track("submit_assignment", {"course_id": course_id, "lesson_id": lesson_id, "url": url})
    st.success("Submitted!")
