import streamlit as st

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

st.title("📋 Personal & Academic Profile")

st.write("🎯 Fill this information for career recommendations.")

# --------------------------------
# PERSONALITY
# --------------------------------

st.header("Personality")

public_speaking = st.slider("Public Speaking Confidence",1,5)

personality = st.selectbox(
"Personality Type",
["Introvert","Extrovert","Ambivert"]
)

team_comfort = st.slider("Teamwork Comfort",1,5)

team_note = st.text_area("Write about your teamwork experience")


# writing score

if len(team_note.split()) < 10:
    writing_score = 0.4
elif len(team_note.split()) < 20:
    writing_score = 0.7
else:
    writing_score = 1


st.session_state["public_speaking"] = public_speaking
st.session_state["team_comfort"] = team_comfort
st.session_state["writing_score"] = writing_score


# --------------------------------
# HOBBIES
# --------------------------------

st.header("Hobbies")

hobbies = st.multiselect(

"Select your hobbies",

[
"Coding",
"Reading",
"Drawing",
"Writing",
"Gaming",
"Robotics",
"Teaching",
"Public Speaking",
"Business",
"Helping People",
"Photography",
"Design",
"Sports"
]

)

st.session_state["hobbies"] = hobbies


# --------------------------------
# PARENT BACKGROUND
# --------------------------------

st.header("Parents Background")

parent_field = st.selectbox(

"Parents Occupation",

[
"Engineering",
"Healthcare",
"Business",
"Education",
"Government",
"Arts / Media",
"Other"
]

)

st.session_state["parent_field"] = parent_field


# --------------------------------
# ACADEMIC MARKS
# --------------------------------

st.header("Academic Performance")

math = st.number_input("Math",0,100)
physics = st.number_input("Physics",0,100)
chemistry = st.number_input("Chemistry",0,100)
biology = st.number_input("Biology",0,100)
cs = st.number_input("Computer Science / IT",0,100)
social_science = st.number_input("Social Science",0,100)

st.session_state["math"] = math
st.session_state["physics"] = physics
st.session_state["chemistry"] = chemistry
st.session_state["biology"] = biology
st.session_state["cs"] = cs
st.session_state["social_science"] = social_science


# --------------------------------
# CAREER INTEREST
# --------------------------------

st.header("Career Interest")

it_interest = st.slider("IT & Computer",1,5)
health_interest = st.slider("Healthcare",1,5)
engineering_interest = st.slider("Engineering",1,5)
creative_interest = st.slider("Creative",1,5)

st.session_state["it_interest"] = it_interest
st.session_state["health_interest"] = health_interest
st.session_state["engineering_interest"] = engineering_interest
st.session_state["creative_interest"] = creative_interest


# --------------------------------
# TOPIC INTEREST
# --------------------------------

st.header("Topic Interest")

math_stats = st.slider("Statistics",1,5)
math_alg = st.slider("Algebra",1,5)
math_calc = st.slider("Calculus",1,5)

cs_prog = st.slider("Programming",1,5)
cs_ai = st.slider("Artificial Intelligence",1,5)
cs_data = st.slider("Data Science",1,5)

bio_human = st.slider("Human Biology",1,5)

arts_interest = st.slider("Arts / Media",1,5)

st.session_state["math_stats"] = math_stats
st.session_state["math_alg"] = math_alg
st.session_state["math_calc"] = math_calc

st.session_state["cs_prog"] = cs_prog
st.session_state["cs_ai"] = cs_ai
st.session_state["cs_data"] = cs_data

st.session_state["bio_human"] = bio_human
st.session_state["arts_interest"] = arts_interest


# --------------------------------
# NEXT BUTTON
# --------------------------------

if st.button("Generate Career Recommendation"):

    st.switch_page("pages/9_Career_Result.py")
