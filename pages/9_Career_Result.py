import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os

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

conn = sqlite3.connect(
    "career_data.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS results(

id INTEGER PRIMARY KEY AUTOINCREMENT,

analytical REAL,
numerical REAL,
creativity REAL,
communication REAL,
social REAL,
persistence REAL,
attention REAL,

math INTEGER,
physics INTEGER,
chemistry INTEGER,
biology INTEGER,
cs INTEGER,

it_interest INTEGER,
health_interest INTEGER,
engineering_interest INTEGER,
creative_interest INTEGER,

parent_field TEXT,
hobbies TEXT,

top_career TEXT,
match_score REAL,

topic_score REAL,
demand_score REAL,
boost_score REAL,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

conn.commit()

# --------------------------------
# CHECK IF ALL TESTS COMPLETED
# --------------------------------

required = [
"analytical",
"numerical",
"creativity",
"communication",
"persistence",
"social",
"attention"
]

missing = [k for k in required if k not in st.session_state]

if missing:
    st.error("Please complete all skill tests before viewing results.")
    st.stop()

st.title("📊 AI Career Recommendation Dashboard")

# --------------------------------
# LOAD DATA
# --------------------------------

file_path = "AI_Career_Master_Dataset_AI_filled.xlsx"

careers = pd.read_excel(file_path)

careers.columns = careers.columns.str.lower()


# --------------------------------
# SAFE SKILL LOADER
# --------------------------------

def get_skill(name):

    v = st.session_state.get(name,0)

    if v is None:
        return 0

    return float(v)


# --------------------------------
# GET SKILL TEST RESULTS
# --------------------------------

analytical = get_skill("analytical")
numerical = get_skill("numerical")
creativity = get_skill("creativity")
communication = get_skill("communication")
persistence = get_skill("persistence")
social = get_skill("social")
attention = get_skill("attention")


# --------------------------------
# GET PROFILE DATA
# --------------------------------

math = st.session_state.get("math",0)
physics = st.session_state.get("physics",0)
chemistry = st.session_state.get("chemistry",0)
biology = st.session_state.get("biology",0)
cs = st.session_state.get("cs",0)

hobbies = st.session_state.get("hobbies",[])

parent_field = st.session_state.get("parent_field","")

it_interest = st.session_state.get("it_interest",3)
health_interest = st.session_state.get("health_interest",3)
engineering_interest = st.session_state.get("engineering_interest",3)
creative_interest = st.session_state.get("creative_interest",3)

math_stats = st.session_state.get("math_stats",3)
math_alg = st.session_state.get("math_alg",3)
math_calc = st.session_state.get("math_calc",3)

cs_prog = st.session_state.get("cs_prog",3)
cs_ai = st.session_state.get("cs_ai",3)
cs_data = st.session_state.get("cs_data",3)

bio_human = st.session_state.get("bio_human",3)

arts_interest = st.session_state.get("arts_interest",3)

public_speaking = st.session_state.get("public_speaking",3)
team_comfort = st.session_state.get("team_comfort",3)
writing_score = st.session_state.get("writing_score",0.5)

hobby_text = ",".join(hobbies)
# --------------------------------
# COSINE SIMILARITY
# --------------------------------

def cosine(a,b):

    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0

    return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))


# --------------------------------
# STUDENT SKILL VECTOR
# --------------------------------

student_vector = np.array([

analytical,
numerical,
creativity,
communication,
social,
attention,
persistence

], dtype=float)


# --------------------------------
# CAREER SCORING
# --------------------------------

topic_scores = []
demand_scores = []
boost_scores = []
final_scores = []

for _,row in careers.iterrows():

    career = str(row["career_name"]).lower()
    cat = str(row["category"])


    career_vector = np.array([

    row["analytical_required"],
    row["numerical_required"],
    row["creativity_required"],
    row["communication_required"],
    row["social_required"],
    row["attention_required"],
    row["persistence_required"]

    ], dtype=float)


    # --------------------------------
    # SKILL SIMILARITY
    # --------------------------------

    skill_score = cosine(student_vector,career_vector)
    skill_score *= 0.35


    # --------------------------------
    # CAREER INTEREST
    # --------------------------------

    if cat == "IT & Computer":
        interest_score = it_interest/5

    elif cat == "Healthcare":
        interest_score = health_interest/5

    elif cat == "Engineering":
        interest_score = engineering_interest/5

    elif cat == "Media & Creative":
        interest_score = creative_interest/5

    else:
        interest_score = 0.5

    interest_score *= 0.15


    # --------------------------------
    # TOPIC INTEREST
    # --------------------------------

    topic_score = 0

    if "data" in career:
        topic_score += cs_data * 0.2

    if "ai" in career:
        topic_score += cs_ai * 0.2

    if "developer" in career:
        topic_score += cs_prog * 0.2

    if "doctor" in career:
        topic_score += bio_human * 0.2

    if "design" in career:
        topic_score += arts_interest * 0.2

    topic_score = min(topic_score/5,1)
    topic_score *= 0.10


    # --------------------------------
    # ACADEMIC SCORE
    # --------------------------------

    if cat == "IT & Computer":

        academic_score = (math + cs + physics)/300

    elif cat == "Engineering":

        academic_score = (math + physics + chemistry)/300

    elif cat == "Healthcare":

        academic_score = (biology + chemistry + physics)/300

    else:

        academic_score = 0.5

    academic_score *= 0.15


    # --------------------------------
    # HOBBIES BOOST
    # --------------------------------

    hobby_score = 0

    if "Coding" in hobbies and "developer" in career:
        hobby_score += 0.3

    if "Drawing" in hobbies and "design" in career:
        hobby_score += 0.3

    if "Teaching" in hobbies and "teacher" in career:
        hobby_score += 0.3

    if "Business" in hobbies and "manager" in career:
        hobby_score += 0.3

    if "Helping People" in hobbies and "doctor" in career:
        hobby_score += 0.3

    hobby_score = min(hobby_score,1)

    hobby_score *= 0.10


    # --------------------------------
    # COMMUNICATION SCORE
    # --------------------------------

    comm_score = (

    0.4 * communication +
    0.25 * (public_speaking/5) +
    0.15 * (team_comfort/5) +
    0.2 * writing_score

    )

    comm_score *= 0.05


    # --------------------------------
    # PARENT BOOST
    # --------------------------------

    parent_score = 0

    if parent_field.lower() in str(cat).lower():

        parent_score = 0.03


    # --------------------------------
    # INDUSTRY DEMAND
    # --------------------------------

    demand_score = row["demand_score"]/100
    demand_score *= 0.04


    # --------------------------------
    # FUTURE SCOPE
    # --------------------------------

    future_score = 0.03


    # --------------------------------
    # JOB ROLE BOOST
    # --------------------------------

    boost = 0

    if "ai" in career and cs_ai > 3:
        boost += 0.05

    if "data" in career and math_stats > 3:
        boost += 0.05

    if "developer" in career and cs_prog > 3:
        boost += 0.05

    if "doctor" in career and bio_human > 3:
        boost += 0.05


    # --------------------------------
    # FINAL SCORE
    # --------------------------------
    
    topic_scores.append(topic_score)
    demand_scores.append(demand_score)
    boost_scores.append(boost)
    
    final = (

    skill_score +
    interest_score +
    topic_score +
    academic_score +
    hobby_score +
    comm_score +
    parent_score +
    demand_score +
    future_score +
    boost

    )

    final_scores.append(final)


careers["final_score"] = final_scores
careers["final_score"] = final_scores
careers["topic_score"] = topic_scores
careers["demand_score"] = demand_scores
careers["boost"] = boost_scores

# --------------------------------
# SKILL BAR CHART
# --------------------------------

st.header("Your Skill Profile")

skills = {
"Analytical": analytical,
"Numerical": numerical,
"Creativity": creativity,
"Communication": communication,
"Social": social,
"Persistence": persistence,
"Attention": attention
}

for k,v in skills.items():

    blocks = int(v * 10)

    bar = "█" * blocks

    st.write(f"{k:<15} {bar} ")


# --------------------------------
# TOP CAREERS
# --------------------------------

top = careers.sort_values(
"final_score",
ascending=False
).head(5)

best_career = top.iloc[0]["career_name"]
best_score = round(top.iloc[0]["final_score"] * 100, 2)
best_topic = top.iloc[0]["topic_score"]
best_demand = top.iloc[0]["demand_score"]
best_boost = top.iloc[0]["boost"]

# --------------------------------
# CAREER RESULTS
# --------------------------------

st.header("Top Career Matches")

for _,row in top.iterrows():

    score = round(row["final_score"]*100,1)

    st.subheader(row["career_name"])

    st.write("Match Score:",score,"%")

    st.write("Category:",row["category"])

    st.write("Salary:",row["salary_range_india"])

    #st.write("Demand Score:",row["demand_score"])

    st.write("Future Scope:",row["future_scope"])

    st.write("Study Abroad:",row["study_abroad_courses"])

    st.write("Countries:",row["study_abroad_countries"])

    st.write("Government Jobs:",row["government_jobs"])

    st.write("---")
    
    
st.divider()

# prevent duplicate saving
if "saved" not in st.session_state:
    st.session_state.saved = False


if not st.session_state.saved:

    if st.button("💾 Save Result to Database"):

        cursor.execute("""

        INSERT INTO results(

        analytical,
        numerical,
        creativity,
        communication,
        social,
        persistence,
        attention,

        math,
        physics,
        chemistry,
        biology,
        cs,

        it_interest,
        health_interest,
        engineering_interest,
        creative_interest,

        parent_field,
        hobbies,

        top_career,
        match_score,

        topic_score,
        demand_score,
        boost_score

        )

        VALUES (?,?,?,?,?,?,?,
                ?,?,?,?,?,
                ?,?,?,?,
                ?,?,
                ?,?,
                ?,?,?)

        """,(

        analytical,
        numerical,
        creativity,
        communication,
        social,
        persistence,
        attention,

        math,
        physics,
        chemistry,
        biology,
        cs,

        it_interest,
        health_interest,
        engineering_interest,
        creative_interest,

        parent_field,
        hobby_text,

        best_career,
        best_score,

        best_topic,
        best_demand,
        best_boost

        ))

        conn.commit()

        st.success("✅ Data saved successfully!")

        st.session_state.saved = True
        file = "student_dataset.csv"

        new_data = {

        "analytical":analytical,
        "numerical":numerical,
        "creativity":creativity,
        "communication":communication,
        "social":social,
        "persistence":persistence,
        "attention":attention,

        "math":math,
        "physics":physics,
        "chemistry":chemistry,
        "biology":biology,
        "cs":cs,

        "it_interest":it_interest,
        "health_interest":health_interest,
        "engineering_interest":engineering_interest,
        "creative_interest":creative_interest,

        "parent_field":parent_field,
        "hobbies":hobby_text,

        "top_career":best_career,
        "match_score":best_score,

        "topic_score":best_topic,
        "demand_score":best_demand,
        "boost_score":best_boost

        }

        df_new = pd.DataFrame([new_data])

        if os.path.exists(file):

            df_old = pd.read_csv(file)

            df_all = pd.concat([df_old,df_new],ignore_index=True)

        else:

            df_all = df_new

        df_all.to_csv(file,index=False)

        st.success("✅ Data saved successfully!")

else:

    st.info("This result has already been saved.")
    

if st.button("🔄 New Student Data"):

    st.session_state.clear()
    st.switch_page("main_app.py")
try:
    df = pd.read_csv("student_dataset.csv")
except:
    st.success("No data")

st.download_button(
"Download Dataset",
df.to_csv(index=False),
"career_dataset.csv"
)
