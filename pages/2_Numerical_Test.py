import streamlit as st
import random
from question_bank import question_bank

skill = "numerical"
total = 10

st.title("🔢 numerical Skill Test")

questions = question_bank[skill]

# generate questions once
if "numerical_q" not in st.session_state:
    st.session_state.numerical_q = random.sample(questions,total)

selected = st.session_state.numerical_q

# submission state
submitted = st.session_state.get("numerical_submitted",False)

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

            st.session_state["numerical"] = score/total

            st.session_state["numerical_submitted"] = True

            st.success(f"Score {score}/{total}")

# -------- NEXT --------

if st.session_state.get("numerical_submitted",False):

    if st.button("Next Test"):

        st.switch_page("pages/3_Creativity_Test.py")