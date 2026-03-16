import streamlit as st
import random
from question_bank import question_bank

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

skill = "social"
total = 5

st.title("🤝 Social Skill Test")

questions = question_bank[skill]

# generate questions once
if "social_q" not in st.session_state:
    st.session_state.social_q = random.sample(questions,total)

selected = st.session_state.social_q

# submission state
submitted = st.session_state.get("social_submitted",False)

answers = []

score = 0

for i,q in enumerate(selected):

    st.write(f"Q{i+1}. {q['q']}")

    options = [f"{k}) {v}" for k,v in q["options"].items()]

    ans = st.radio(

        "Choose",

        options,

        index=None,

        key=f"{skill}{i}",

        disabled=submitted

    )

    answers.append(ans)

# -------- SUBMIT --------

if not submitted:

    if st.button("Submit"):

        if None in answers:

            st.error("Please answer all questions")

        else:

            for i,q in enumerate(selected):

                ans = st.session_state[f"{skill}{i}"]

                if ans[0] == q["ans"]:

                    score += 1

            st.session_state["social"] = score/total

            st.session_state["social_submitted"] = True

            st.success(f"Score {score}/{total}")

# -------- NEXT --------

if st.session_state.get("social_submitted",False):

    if st.button("Next Test"):

        st.switch_page("pages/7_Attention_Test.py")
