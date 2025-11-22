import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Gym Logger", layout="wide")

# ---------- Background ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1517836357463-d25dfeac3438');
    background-size: cover;
    background-position: center;
}
.section {
    background: rgba(0,0,0,0.55);
    padding: 20px;
    border-radius: 12px;
    backdrop-filter: blur(6px);
    margin-bottom: 25px;
}
label, .stTextInput, .stNumberInput, .stDataFrame { color:white !important; }
</style>
""", unsafe_allow_html=True)

# ---------- Session Storage ----------
if "log" not in st.session_state:
    st.session_state.log = pd.DataFrame(columns=["Date", "Exercise", "Sets", "Reps", "Weight", "Volume"])

# ---------- Title ----------
st.markdown("<h1 style='text-align:center; color:white;'>🏋️ Gym Workout Logger</h1>", unsafe_allow_html=True)


# ============================================================
# 🔹 SECTION 1 — Add Workout
# ============================================================
with st.container():
    st.markdown("<div class='section'>", unsafe_allow_html=True)

    st.markdown("## ✏️ Log Workout")

    col1, col2, col3, col4 = st.columns(4)
    ex = col1.text_input("Exercise")
    sets = col2.number_input("Sets", 1)
    reps = col3.number_input("Reps", 1)
    wt = col4.number_input("Weight (kg)", 1)

    if st.button("Add Entry 💾"):
        volume = sets * reps * wt
        row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Exercise": ex,
            "Sets": sets,
            "Reps": reps,
            "Weight": wt,
            "Volume": volume
        }
        st.session_state.log = pd.concat([st.session_state.log, pd.DataFrame([row])], ignore_index=True)
        st.success("Workout added!")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# 🔹 SECTION 2 — Workout Table
# ============================================================
with st.container():
    st.markdown("<div class='section'>", unsafe_allow_html=True)

    st.markdown("## 📋 Workout History")
    st.dataframe(st.session_state.log, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# 🔹 SECTION 3 — Weekly Progress Chart
# ============================================================
with st.container():
    st.markdown("<div class='section'>", unsafe_allow_html=True)

    st.markdown("## 📈 Weekly Progress")

    if len(st.session_state.log):
        df = st.session_state.log.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        weekly = df.groupby("Date")["Volume"].sum()

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(weekly.index, weekly.values, linewidth=3)
        ax.set_title("Training Volume Over Time")
        ax.set_ylabel("Total Volume")
        ax.grid(True)

        st.pyplot(fig)
    else:
        st.info("No workout entries yet!")

    st.markdown("</div>", unsafe_allow_html=True)
