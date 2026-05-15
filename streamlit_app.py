import os
import pandas as pd
import streamlit as st

DATA_FILE = "European_Bank .. vs churn.xlsx"

@st.cache_data
def load_data():
    if not os.path.exists(DATA_FILE):
        st.error(f"Dataset not found: {DATA_FILE}")
        return pd.DataFrame()
    return pd.read_excel(DATA_FILE, engine="openpyxl")

@st.cache_data
def summary_stats(data: pd.DataFrame):
    return {
        "Total customers": len(data),
        "Churn rate": f"{data['Exited'].mean() * 100:.2f}%",
        "Average balance": f"${data['Balance'].mean():,.2f}",
        "Average salary": f"${data['EstimatedSalary'].mean():,.2f}",
    }

st.set_page_config(page_title="Bank Customer Churn Explorer", layout="wide")
st.title("European Bank Customer Churn Explorer")
st.markdown(
    "Use this dashboard to explore churn behavior, customer segments, and key metrics "
    "for the bank dataset."
)

data = load_data()
if data.empty:
    st.stop()

# Sidebar filters
st.sidebar.header("Filter customers")
selected_geographies = st.sidebar.multiselect(
    "Geography", sorted(data["Geography"].dropna().unique()), default=sorted(data["Geography"].dropna().unique())
)
selected_gender = st.sidebar.multiselect(
    "Gender", sorted(data["Gender"].dropna().unique()), default=sorted(data["Gender"].dropna().unique())
)
selected_card = st.sidebar.multiselect(
    "Has credit card", sorted(data["HasCrCard"].dropna().unique()), default=sorted(data["HasCrCard"].dropna().unique())
)
selected_active = st.sidebar.multiselect(
    "Is active member", sorted(data["IsActiveMember"].dropna().unique()), default=sorted(data["IsActiveMember"].dropna().unique())
)

filtered = data[
    data["Geography"].isin(selected_geographies)
    & data["Gender"].isin(selected_gender)
    & data["HasCrCard"].isin(selected_card)
    & data["IsActiveMember"].isin(selected_active)
]

st.subheader("Key metrics")
metrics = summary_stats(filtered)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total customers", metrics["Total customers"])
col2.metric("Churn rate", metrics["Churn rate"])
col3.metric("Average balance", metrics["Average balance"])
col4.metric("Average salary", metrics["Average salary"])

st.subheader("Dataset preview")
st.dataframe(filtered.head(100), use_container_width=True)

st.subheader("Churn and customer segments")
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.markdown("**Exited distribution**")
    churn_counts = filtered["Exited"].value_counts().rename({0: "Stayed", 1: "Exited"})
    st.bar_chart(churn_counts)
with chart_col2:
    st.markdown("**Customers by geography**")
    geography_counts = filtered["Geography"].value_counts()
    st.bar_chart(geography_counts)

st.subheader("Numeric insights")
insight_col1, insight_col2 = st.columns(2)
with insight_col1:
    st.markdown("**Age distribution**")
    st.bar_chart(filtered["Age"].value_counts().sort_index())
with insight_col2:
    st.markdown("**Balance vs salary**")
    st.write(filtered[["Balance", "EstimatedSalary"]].describe())

st.subheader("Filtered data details")
st.write(filtered)

st.markdown("---")
st.markdown(
    "**Columns:** Year, CustomerId, Surname, CreditScore, Geography, Gender, Age, "
    "Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited"
)
