import streamlit as st
import pandas as pd
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="💸 Friends Expense Splitter", layout="wide")

# --- Custom CSS for Styling ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
    background-attachment: fixed;
    color: #2b2b2b;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
h1, h2, h3 {
    color: #3a0ca3;
    text-align: center;
    font-family: 'Poppins', sans-serif;
}
.stButton>button {
    background-color: #7209b7;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #560bad;
    transform: scale(1.05);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Header ---
st.title("💸 Friends Expense Splitter")
st.subheader("Split bills easily and keep the fun going! 🎉")

# --- Input Section ---
col1, col2 = st.columns(2)
with col1:
    total_amount = st.number_input("Enter Total Expense Amount (₹)", min_value=0.0, step=10.0, format="%.2f")

with col2:
    num_people = st.number_input("Number of People", min_value=1, step=1, format="%d")

if num_people > 0:
    st.markdown("### 👥 Add Names and Contributions (optional)")
    names = []
    contributions = []
    for i in range(num_people):
        c1, c2 = st.columns([2, 1])
        with c1:
            name = st.text_input(f"Name of Person {i+1}", value=f"Friend {i+1}")
            names.append(name)
        with c2:
            contrib = st.number_input(f"{name}'s Contribution (₹)", min_value=0.0, step=10.0, key=f"contrib_{i}")
            contributions.append(contrib)

    # --- Calculation ---
    if st.button("💥 Calculate Split"):
        df = pd.DataFrame({
            "Name": names,
            "Contribution": contributions
        })
        total_contrib = df["Contribution"].sum()
        if total_contrib == 0:
            total_contrib = total_amount  # fallback if no contribution entered
        equal_share = total_contrib / num_people
        df["Share"] = np.round(equal_share, 2)
        df["Balance"] = np.round(df["Contribution"] - df["Share"], 2)

        st.markdown("### 🧾 Split Summary")
        st.dataframe(df.style.background_gradient(cmap="coolwarm"))

        st.markdown("---")
        owes = df[df["Balance"] < 0]
        gets = df[df["Balance"] > 0]

        if not owes.empty or not gets.empty:
            st.markdown("### 💰 Settlement Suggestions")
            transactions = []
            owes = owes.copy()
            gets = gets.copy()

            for _, debtor in owes.iterrows():
                for _, creditor in gets.iterrows():
                    if debtor["Balance"] == 0:
                        break
                    amount = min(-debtor["Balance"], creditor["Balance"])
                    if amount > 0:
                        transactions.append(f"➡️ **{debtor['Name']}** pays ₹{amount:.2f} to **{creditor['Name']}**")
                        debtor["Balance"] += amount
                        gets.loc[creditor.name, "Balance"] -= amount

            for t in transactions:
                st.markdown(t)

        st.success("✅ Split complete! Everyone’s balances are shown above.")

# --- Footer ---
st.markdown("<br><hr><center>Made with ❤️ using Streamlit</center>", unsafe_allow_html=True)
