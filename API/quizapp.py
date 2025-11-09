import streamlit as st

st.set_page_config(page_title="Quiz App", page_icon="🧠")

st.title("🧠 Quiz App")
st.subheader("Python Developer MCQ Quiz (5 Questions)")

# define quiz data
questions = [
    {
        "q": "Which library is used for DataFrame in Python?",
        "options": ["Numpy", "Pandas", "Matplotlib", "Streamlit"],
        "answer": "Pandas"
    },
    {
        "q": "Which operator is used for exponent in python?",
        "options": ["^", "**", "//", "%%"],
        "answer": "**"
    },
    {
        "q": "Which keyword is used to create a function?",
        "options": ["func", "def", "function", "lambda"],
        "answer": "def"
    },
    {
        "q": "What is output of len('Python')?",
        "options": ["5", "6", "7", "Error"],
        "answer": "6"
    },
    {
        "q": "Which is used to install packages in python?",
        "options": ["pip", "exe", "install", "python-install"],
        "answer": "pip"
    }
]

# session to safe score & flow
if "submitted" not in st.session_state:
    st.session_state.submitted = False

user_answers = []

for i, q in enumerate(questions):
    ans = st.radio(q["q"], q["options"], index=None, key=f"q_{i}")
    user_answers.append(ans)

if st.button("Submit"):
    st.session_state.submitted = True

if st.session_state.submitted:
    score = 0
    for i, q in enumerate(questions):
        if user_answers[i] == q["answer"]:
            score += 1

    st.write("### ✅ Score :", score, "/ 5")

    if score == 5:
        st.success("Excellent 🎉 Perfect Score!!")
    elif score >= 3:
        st.info("Good Job 🙂")
    else:
        st.warning("Improve and retake 🤓")

    if st.button("Try Again"):
        st.session_state.submitted = False
        st.rerun()
