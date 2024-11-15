import streamlit as st
st.set_page_config(
    page_title="Study Pal",
    page_icon="🌱", #deleted markdown syntax
)
session_id_runn="runn_chat_history"
session_id_wo_runn="wo_runn_chat_history"
st.title("Study Pal🌱📚💪")
st.subheader("Learning is Fun!")
languages=["English","Telugu","Hindi","Malayalam","Marathi","Bengali","Kannada"]
instructions_lis=["Tutor Me","Teacher Pal","Translate","Learn Language","Communicate","Surprise Me","Tell Me Why","Tongue Twister","Humor Me","Story Time", "More Fun Games","Inspire Me"]
instruction = st.selectbox("Pages",instructions_lis)
