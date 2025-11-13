import streamlit as st

# Page setup
st.set_page_config(page_title="Greeting Form", page_icon="🎨", layout="centered")

# Custom background and form styling
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1503264116251-35a269479413?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
}

[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}

h1, h3, label, p {
    color: white !important;
    text-shadow: 1px 1px 3px #000000;
}

div.stButton > button {
    background-color: #ff6f61;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    background-color: #ff9a76;
    transform: scale(1.05);
}

div.stTextInput, div.stSlider {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 10px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Title
st.title("🌈 Greeting")
st.markdown("### Life is colorful!")

# Form section
with st.form("greeting_form"):
    name = st.text_input("Your Name:")
    age = st.slider("Your Age:", 1, 100, 25)
    submit = st.form_submit_button("✨ Show Greeting")

if submit:
    st.success(f"Hello, **{name}**! You’re **{age}** years young! 🌟")
    st.balloons()
