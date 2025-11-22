import streamlit as st

st.set_page_config(page_title="BMI Calculator", page_icon="🏋️")

st.title("🏋️ BMI Calculator")
st.write("Enter your height and weight to calculate your Body Mass Index (BMI).")

# Inputs
height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, step=0.1)
weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, step=0.1)

if st.button("Calculate BMI"):
    if height > 0 and weight > 0:
        height_m = height / 100  # convert cm to meters
        bmi = weight / (height_m ** 2)

        st.subheader(f"Your BMI: **{bmi:.2f}**")

        # Determine category
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        st.write(f"**Category:** {category}")
    else:
        st.error("Please enter valid height and weight values.")
