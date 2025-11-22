import streamlit as st

# --- Page setup ---
st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")

# --- Custom background and styling ---
page_style = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}
[data-testid="stHeader"], [data-testid="stToolbar"] {
    background: rgba(0,0,0,0);
}
h1, h2, h3, label, p {
    color: #fff !important;
    text-shadow: 1px 1px 3px #000;
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
    background-color: #ffa372;
    transform: scale(1.05);
}
div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.1);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# --- App Title ---
st.title("🧮 Simple Calculator")
st.markdown("### Perform basic operations with style! ✨")

# --- Calculator Form ---
with st.form("calc_form"):
    num1 = st.number_input("Enter first number", value=0.0, step=1.0)
    num2 = st.number_input("Enter second number", value=0.0, step=1.0)
    operation = st.selectbox("Select Operation", ["➕ Add", "➖ Subtract", "✖️ Multiply", "➗ Divide"])
    calc = st.form_submit_button("💫 Calculate")

# --- Calculation Logic ---
if calc:
    if operation == "➕ Add":
        result = num1 + num2
    elif operation == "➖ Subtract":
        result = num1 - num2
    elif operation == "✖️ Multiply":
        result = num1 * num2
    elif operation == "➗ Divide":
        if num2 != 0:
            result = num1 / num2
        else:
            st.error("🚫 Division by zero is not allowed!")
            st.stop()
    
    st.success(f"✅ **Result:** {result}")
    st.balloons()
