# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BlinkIt - Sales Dashboard", page_icon="🟡", layout="wide")

# --------------------------
# Yellow-ish theme (Blinkit)
# --------------------------
st.markdown(
    """
    <style>
    :root {
        --accent: #ffcc00;
        --accent-dark: #f0b400;
        --bg: #fff9e6;
        --card: #fff;
        --muted: #666666;
    }
    .stApp {
        background-color: var(--bg);
    }
    header, .css-1v3fvcr {  /* header bar */
        background: linear-gradient(90deg, var(--accent), var(--accent-dark));
        color: #222 !important;
    }
    .stSidebar .css-1d391kg { background-color: #fff8e0; }
    .kpi {
        background: linear-gradient(180deg, #fff, #fff8e6);
        border-radius: 10px;
        padding: 14px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .small-muted { color: var(--muted); font-size:12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------
# Load data
# --------------------------
DATA_PATH = r"D:\pythonlearning\RPA_Demo\BlinkIT Grocery Data.xlsx"

@st.cache_data(ttl=600)
def load_data(path=DATA_PATH):
    # try multiple sheet names; default to first sheet
    try:
        df = pd.read_excel(path, engine="openpyxl")
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return pd.DataFrame()

    # remove fully blank rows
    df = df.dropna(how="all")

    # drop rows missing core columns if they exist in file
    required_candidates = ["Item_Identifier", "Item_Outlet_Sales", "Item_Type", "Outlet_Size"]
    present_required = [c for c in required_candidates if c in df.columns]
    if present_required:
        df = df.dropna(subset=present_required)

    # normalize column names (strip)
    df.columns = [c.strip() for c in df.columns]

    return df

df = load_data()

if df.empty:
    st.warning("Dataframe is empty or couldn't be loaded. Please ensure `/mnt/data/BlinkIT Grocery Data.xlsx` exists and has data.")
    st.stop()

# --------------------------
# Sidebar filters
# --------------------------
st.sidebar.header("FILTER PANEL")
# helper to build multiselect with safe defaults
def ms(name):
    if name in df.columns:
        choices = sorted(df[name].dropna().astype(str).unique())
        return st.sidebar.multiselect(name, choices, default=choices)
    return None

outlet_size_sel = ms("Outlet_Size")
outlet_type_sel = ms("Outlet_Type")
outlet_loc_sel = ms("Outlet_Location_Type")
item_type_sel = ms("Item_Type")
fat_content_sel = ms("Item_Fat_Content")
# date-like or year filter if present
est_year_sel = None
if "Outlet_Establishment_Year" in df.columns:
    years = sorted(df["Outlet_Establishment_Year"].dropna().unique())
    est_year_sel = st.sidebar.multiselect("Outlet_Establishment_Year", years, default=years)

# --------------------------
# Filtering function
# --------------------------
def apply_filters(df):
    d = df.copy()
    if outlet_size_sel is not None:
        d = d[d["Outlet_Size"].astype(str).isin(outlet_size_sel)]
    if outlet_type_sel is not None:
        d = d[d["Outlet_Type"].astype(str).isin(outlet_type_sel)]
    if outlet_loc_sel is not None:
        d = d[d["Outlet_Location_Type"].astype(str).isin(outlet_loc_sel)]
    if item_type_sel is not None:
        d = d[d["Item_Type"].astype(str).isin(item_type_sel)]
    if fat_content_sel is not None:
        d = d[d["Item_Fat_Content"].astype(str).isin(fat_content_sel)]
    if est_year_sel is not None:
        d = d[d["Outlet_Establishment_Year"].isin(est_year_sel)]
    return d

df_filtered = apply_filters(df)

# --------------------------
# KPIs (Top row)
# --------------------------
# Compute safe KPIs depending on available columns
total_sales = df_filtered["Item_Outlet_Sales"].sum() if "Item_Outlet_Sales" in df_filtered.columns else 0
num_items = df_filtered["Item_Identifier"].nunique() if "Item_Identifier" in df_filtered.columns else df_filtered.shape[0]
avg_sales = df_filtered["Item_Outlet_Sales"].mean() if "Item_Outlet_Sales" in df_filtered.columns else 0

# optional rating column detection
rating_col = None
for possible in ["Item_Outlet_Rating", "Avg_Rating", "Rating"]:
    if possible in df_filtered.columns:
        rating_col = possible
        break
avg_rating = df_filtered[rating_col].mean() if rating_col else None

k1, k2, k3, k4 = st.columns([1.6,1.2,1.2,1.2])
with k1:
    st.markdown("<div class='kpi'><h3 style='margin:0;'>BlinkIt Sales</h3><div class='small-muted'>Total Sales</div>"
                f"<h2>₹ {total_sales:,.0f}</h2></div>", unsafe_allow_html=True)
with k2:
    st.markdown("<div class='kpi'><div class='small-muted'>Number of Items</div>"
                f"<h3>{num_items:,}</h3></div>", unsafe_allow_html=True)
with k3:
    st.markdown("<div class='kpi'><div class='small-muted'>Avg Sales</div>"
                f"<h3>₹ {avg_sales:,.0f}</h3></div>", unsafe_allow_html=True)
with k4:
    if avg_rating is not None:
        st.markdown("<div class='kpi'><div class='small-muted'>Avg Rating</div>"
                    f"<h3>{avg_rating:.2f} / 5</h3></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='kpi'><div class='small-muted'>Avg Rating</div><h3>—</h3></div>", unsafe_allow_html=True)

st.markdown("---")

# --------------------------
# Left column small charts / breakdowns
# --------------------------
left, right = st.columns([1,2])

with left:
    st.subheader("Sales by Outlet Type")
    if "Outlet_Type" in df_filtered.columns and "Item_Outlet_Sales" in df_filtered.columns:
        agg = df_filtered.groupby("Outlet_Type")["Item_Outlet_Sales"].sum().reset_index()
        fig = px.pie(agg, names="Outlet_Type", values="Item_Outlet_Sales", hole=0.55)
        fig.update_layout(margin=dict(l=0,r=0,t=30,b=0), legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No Outlet_Type or Sales column found for pie chart.")

    st.write("")
    st.subheader("Top Products (by Sales)")
    if "Item_Type" in df_filtered.columns and "Item_Outlet_Sales" in df_filtered.columns:
        top_prod = (df_filtered.groupby("Item_Type")["Item_Outlet_Sales"]
                    .sum().reset_index().sort_values("Item_Outlet_Sales", ascending=False).head(10))
        fig2 = px.bar(top_prod, x="Item_Outlet_Sales", y="Item_Type", orientation="h")
        fig2.update_layout(margin=dict(l=0,r=0,t=10,b=0), yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No Item_Type or Sales column found for top products.")

with right:
    st.subheader("Sales Trend by Month/Outlet (if available)")
    # If a date-like column exists, try to plot time series. Else, try by establishment year or month column.
    # Look for typical columns
    if "Date" in df_filtered.columns:
        df_filtered["Date2"] = pd.to_datetime(df_filtered["Date"], errors="coerce")
        ts = df_filtered.dropna(subset=["Date2"]).groupby(pd.Grouper(key="Date2", freq="M"))["Item_Outlet_Sales"].sum().reset_index()
        if not ts.empty:
            fig3 = px.line(ts, x="Date2", y="Item_Outlet_Sales", markers=True)
            fig3.update_layout(margin=dict(l=0,r=0,t=10,b=0))
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No parsable Date column for trend.")
    elif "Outlet_Establishment_Year" in df_filtered.columns:
        trend = df_filtered.groupby("Outlet_Establishment_Year")["Item_Outlet_Sales"].sum().reset_index().sort_values("Outlet_Establishment_Year")
        fig3 = px.line(trend, x="Outlet_Establishment_Year", y="Item_Outlet_Sales", markers=True)
        fig3.update_layout(margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig3, use_container_width=True)
    else:
        # fallback: monthly-like string column
        if "Month" in df_filtered.columns:
            m = df_filtered.groupby("Month")["Item_Outlet_Sales"].sum().reset_index()
            fig3 = px.line(m, x="Month", y="Item_Outlet_Sales", markers=True)
            fig3.update_layout(margin=dict(l=0,r=0,t=10,b=0), xaxis={'categoryorder':'array','categoryarray':m['Month'].tolist()})
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No Date/Month/Establishment year column available for trend chart.")

st.markdown("---")

# --------------------------
# Cross table & metrics
# --------------------------
st.subheader("Outlet Performance & Breakdown")
cols = st.columns(3)
with cols[0]:
    if "Outlet_Size" in df_filtered.columns:
        size_agg = df_filtered.groupby("Outlet_Size")["Item_Outlet_Sales"].sum().reset_index()
        st.dataframe(size_agg, use_container_width=True)
    else:
        st.info("No Outlet_Size column.")

with cols[1]:
    if "Outlet_Type" in df_filtered.columns:
        ot = df_filtered.groupby(["Outlet_Type"])["Item_Outlet_Sales"].agg(["sum","mean","count"]).reset_index()
        ot.columns = ["Outlet_Type","Total Sales","Avg Sales","Transactions"]
        st.dataframe(ot.sort_values("Total Sales", ascending=False), use_container_width=True)
    else:
        st.info("No Outlet_Type column.")

with cols[2]:
    if "Item_Fat_Content" in df_filtered.columns:
        fat = df_filtered.groupby("Item_Fat_Content")["Item_Outlet_Sales"].sum().reset_index()
        figf = px.bar(fat, x="Item_Fat_Content", y="Item_Outlet_Sales")
        figf.update_layout(margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(figf, use_container_width=True)
    else:
        st.info("No Item_Fat_Content column.")

st.markdown("---")

# --------------------------
# Detailed table (cleaned / no blanks)
# --------------------------
st.subheader("Detailed Data (cleaned)")
# remove rows that are almost blank already done earlier; show subset
show_cols = df_filtered.columns.tolist()
st.dataframe(df_filtered[show_cols].reset_index(drop=True), use_container_width=True)

# --------------------------
# Footer / download
# --------------------------
st.markdown("### Download filtered data")
csv = df_filtered.to_csv(index=False)
st.download_button("Download CSV of filtered data", csv, "blinkit_filtered.csv", "text/csv")
