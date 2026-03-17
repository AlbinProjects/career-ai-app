import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<style>

/* Disable clicking on sidebar page navigation */
[data-testid="stSidebarNav"] a {
    pointer-events: none;
    cursor: default;
}

/* Optional: make it look disabled */
[data-testid="stSidebarNav"] a:hover {
    background-color: transparent;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="AI Career Intelligence System",layout="wide")

st.title("🎓 AI Career Intelligence System")

st.write("""
This system analyzes your:

✔ Skills  
✔ Academic performance  
✔ Interests  
✔ Personality  
✔ Hobbies  

Then recommends the **best careers using AI matching**.
""")

# initialize scores
skills = [
"analytical",
"numerical",
"creativity",
"communication",
"persistence",
"social",
"attention"
]

for s in skills:
    if s not in st.session_state:
        st.session_state[s] = None

completed = sum([1 for s in skills if st.session_state[s] is not None])

progress = completed / len(skills)

st.subheader("Test Progress")

st.progress(progress)

st.write(f"{completed} / {len(skills)} tests completed")

st.info("Complete all tests from the sidebar.")

if st.button("🚀 Start First Test"):

    st.switch_page("pages/1_Analytical_Test.py")
