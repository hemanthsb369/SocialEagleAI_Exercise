import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

st.title("📊 Sales Dashboard")

# ---------------------------------------------
# SAMPLE DATA (You can replace with DB / CSV)
# ---------------------------------------------
data = {
    "Month": ["Jan","Jan","Jan","Feb","Feb","Feb","Mar","Mar","Mar"],
    "Product": ["Laptop","Phone","TV"]*3,
    "Sales": [150000,80000,60000,180000,95000,70000,220000,115000,85000]
}
df = pd.DataFrame(data)

# Filters
col1, col2 = st.columns(2)
with col1:
    month_filter = st.multiselect("Select Month", df["Month"].unique(), default=df["Month"].unique())

with col2:
    prod_filter = st.multiselect("Select Product", df["Product"].unique(), default=df["Product"].unique())

df_filtered = df[(df["Month"].isin(month_filter)) & (df["Product"].isin(prod_filter))]

# KPI
total_sales = df_filtered["Sales"].sum()
avg_sales = df_filtered["Sales"].mean()

c1, c2 = st.columns(2)
c1.metric("Total Sales", f"₹ {total_sales:,.2f}")
c2.metric("Avg Sales", f"₹ {avg_sales:,.2f}")

# Charts
st.subheader("Sales by Product")

prod_sales = df_filtered.groupby("Product")["Sales"].sum()

fig1, ax1 = plt.subplots()
ax1.bar(prod_sales.index, prod_sales.values)
st.pyplot(fig1)

st.subheader("Sales by Month")

month_sales = df_filtered.groupby("Month")["Sales"].sum()

fig2, ax2 = plt.subplots()
ax2.plot(month_sales.index, month_sales.values, marker="o")
st.pyplot(fig2)

# Detailed Table
st.subheader("Detailed Data")
st.dataframe(df_filtered, use_container_width=True)
