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

# List of page files with their display names
page_files_list = [
    {"file": "pages/1_Tutor Me📚👨‍🏫.py", "display_name": "Tutor Me 📚👨‍🏫"},
    {"file": "pages/2_Teacher Pal👩‍🏫👨‍🏫.py", "display_name": "Teacher Pal 👩‍🏫👨‍🏫"},
    {"file": "pages/3_Translate🔄🗣️.py", "display_name": "Translate 🔄🗣️"},
    {"file": "pages/4_Learn Language🗣️📝.py", "display_name": "Learn Language 🗣️📝"},
    {"file": "pages/5_Communicate🗣️💬.py", "display_name": "Communicate 🗣️💬"},
    {"file": "pages/6_Surprise Me🤩🎁.py", "display_name": "Surprise Me 🤩🎁"},
    {"file": "pages/7_Tell Me Why❓🤔💡.py", "display_name": "Tell Me Why ❓🤔💡"},
    {"file": "pages/8_Tongue Twister👅🔄🤪.py", "display_name": "Tongue Twister 👅🔄🤪"},
    {"file": "pages/9_Humor Me😂🤣.py", "display_name": "Humor Me 😂🤣"},
    {"file": "pages/10_Story Time🌙🛌.py", "display_name": "Story Time 🌙🛌"},
    {"file": "pages/11_More Fun Games🎮🧩🎲.py", "display_name": "More Fun Games 🎮🧩🎲"},
    {"file": "pages/12_Inspire Me🌟💪✨.py", "display_name": "Inspire Me 🌟💪✨"}
]



cols=st.columns(3)
i=0
# Display page links
for page in page_files_list:
    if i>=3:
        i=0
    with cols[i]:
        st.page_link(page["file"], label=page["display_name"], icon=None)
        i=i+1
