import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Interactive Sales Dashboard", layout="wide")

st.title("📊 Interactive Sales Dashboard")

# Load Dataset
df = pd.read_csv("data/superstore.csv", encoding="latin1")

# Convert Order Date
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Sidebar Filters
st.sidebar.header("Filter Data")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# KPI Cards
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", total_orders)

st.markdown("---")

# Monthly Sales Trend
monthly_sales = filtered_df.groupby(
    filtered_df["Order Date"].dt.strftime("%b-%Y")
)["Sales"].sum().reset_index()

fig1 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# Sales by Category
category_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()

fig2 = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    title="Sales by Category"
)

st.plotly_chart(fig2, use_container_width=True)

# Region Sales
region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()

fig3 = px.pie(
    region_sales,
    values="Sales",
    names="Region",
    title="Sales by Region"
)

st.plotly_chart(fig3, use_container_width=True)

# Top Products
st.subheader("Top Selling Products")

top_products = filtered_df.groupby("Product Name")["Sales"].sum()

top_products = top_products.sort_values(ascending=False).head(10)

st.dataframe(top_products)

# Download Button
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)
