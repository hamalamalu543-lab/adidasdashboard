import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
import os
#PAGE CONFIG
st.set_page_config(page_title="Sales Model Dashboard",layout="wide")
#DARK THEME - POWER BI STYLE
st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: rgb(100, 212, 155);
    color: white;
}

/* KPI Cards */
.kpi-box{
    background-color:#7d6b87;
    padding:20px;
    border-radius:10px;
    text-align:center;
    color:red;
    box-shadow: 0 0 10px rgba(255, 0, 0);
}

.kpi-title {
    font-size:18px;
    color:#A0A0A0;
}

.kpi-value{
    font-size: 32px;
    font-weight:bold;
    color:#4CAF50;/* Green */
}

/* sidebar */
.css-1d391kg{
    background-color:pink;
}
/* Metric cards */
[data-testid="metric-container"]{
    background-color: #1F2937;
    border: 1px solid #374151;
    padding: 15px;
    border-radius: 10px;
}

/* Headings */
h1,h2,h3,h4{
    color:red;
}
            
/* Dataframe */
[data-testid="stDataFrame"]{
    background-color:#1F2937;
}

/* Buttons */
.stDownloadButton button {
    background-color:#2563EB;
    color: white;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)
#CSV LOAD
# Try auto load from repo first
if "AdidasSalesdata.csv" in os.listdir():
    data = pd.read_csv("AdidasSalesdata.csv")
else:
    st.sidebar.header(" Upload Sales CSV")
    uploaded_file = st.sidebar.file_uploader(
        "Upload AdidasSalesdata.csv",
        type=["csv"]
    )
    if uploaded_file is None:
        st.info("Upload AdidasSalesdata.csv to view dashboard")
        st.stop()
    data = pd.read_csv(uploaded_file)


# Load image
import streamlit as st
import base64

# Convert image to base64
def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64("adidas_shoe.png")

st.markdown(f"""
<div style="display:flex; align-items:center; justify-content:center; gap:15px;">
    <img src="data:image/png;base64,{img_base64}" width="80">
    <h1 style="color:#F5F5F5; margin:0;">
        Adidas Sales Dashboard
    </h1>
</div>
""", unsafe_allow_html=True)


#DATA VALIDATION
required_cols=[
    "order ID","Invoice Date","Region","State","City",
    "Units Sold","Product Category","Total Sales","Sales Method","Operating Profit"
    
]
if not all(col in data.columns for col in required_cols):
    st.error(f"CSV must contain columns:{required_cols}")
    st.stop()


# DATA PREPARATION
data["Invoice Date"] = pd.to_datetime(data["Invoice Date"])

# CREATE MONTH COLUMN
data["Month"] = data["Invoice Date"].dt.strftime("%Y-%m")


#SIDEBAR FILTERS
# SIDEBAR FILTERS
st.header("Filters")

col1, col2 = st.columns(2)

with col1:
    region = st.selectbox(
        "Select Region",
        ["All"] + list(data["Region"].unique())
    )

with col2:
    product_category = st.selectbox(
        "Select Product Category",
        ["All"] + list(data["Product Category"].unique())
    )

# ✅ IMPORTANT: define filtered here
filtered = data.copy()

if region != "All":
    filtered = filtered[filtered["Region"] == region]

if product_category != "All":
    filtered = filtered[filtered["Product Category"] == product_category]

                                                                                                                                                                           
# KPI CARDS (TOP ROW)
st.subheader("Key Performance Indicators")

# Calculate values
total_sales = filtered["Total Sales"].sum()
units_sold = filtered["Units Sold"].sum()
profit = filtered["Operating Profit"].sum()
profit_percent = (profit / total_sales) * 100 if total_sales != 0 else 0

# Create KPI cards (3 in a row)
# KPI CARDS
import streamlit as st

# Calculate values
total_sales = filtered["Total Sales"].sum()
units_sold = filtered["Units Sold"].sum()

# Create 2-column layout
k1, k2 = st.columns(2)

# KPI 1 - Total Sales (Green Glass Effect)
k1.markdown(f"""
<div style="
    background: rgba(76, 175, 80, 0.2);  /* green glass */
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    border: 1px solid rgba(76, 175, 80, 0.4);
    box-shadow: 0 8px 32px 0 rgba(0,0,0,0.25);
">
    <h4>💰 Total Sales</h4>
    <h2>₹ {total_sales:,.0f}</h2>
</div>
""", unsafe_allow_html=True)

# KPI 2 - Units Sold (Green Glass Effect)
k2.markdown(f"""
<div style="
    background: rgba(76, 175, 80, 0.2);  /* green glass */
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    border: 1px solid rgba(76, 175, 80, 0.4);
    box-shadow: 0 8px 32px 0 rgba(0,0,0,0.25);
">
    <h4>📦 Units Sold</h4>
    <h2>{units_sold:,}</h2>
</div>
""", unsafe_allow_html=True)
# GAUGE CHARTS (MODEL STYLE)
import plotly.graph_objects as go
import streamlit as st

# First calculate KPIs
total_sales = filtered["Total Sales"].sum()
units_sold = filtered["Units Sold"].sum()
profit = filtered["Operating Profit"].sum()

# Sales Target %
target_sales = 1000000
sales_percent = (total_sales / target_sales) * 100

# Profit %
profit_percent = (profit / total_sales) * 100 if total_sales != 0 else 0

# Units %
units_percent = (units_sold / filtered["Units Sold"].max()) * 100 if filtered["Units Sold"].max() != 0 else 0

# Gauge function
def gauge(title, value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'suffix': "%", 'font': {'size': 32}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "steps": [
                {"range": [0, 20], "color": "#ff4d4d"},
                {"range": [20, 40], "color": "#ff944d"},
                {"range": [40, 60], "color": "#ffd11a"},
                {"range": [60, 80], "color": "#85e085"},
                {"range": [80, 100], "color": "#33cc33"},
            ],
            "bar": {"color": "black"},
            "threshold": {"line": {"color": "white", "width": 4}, "thickness": 0.75, "value": value}
        },
        title={"text": title, "font": {"size": 20}}
    ))
    fig.update_layout(height=320, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# Now display gauges
g1, g2, g3 = st.columns(3)
g1.plotly_chart(gauge("Sales Target %", sales_percent), use_container_width=True)
g2.plotly_chart(gauge("Profit %", profit_percent), use_container_width=True)
g3.plotly_chart(gauge("Performance %", units_percent), use_container_width=True)
##title color
def colored_title(text, color):
    st.markdown(f"<h3 style='color:{color};'>{text}</h3>", unsafe_allow_html=True)

colored_title("🟣 Region-wise Sales", "purple")
colored_title("🟠 Monthly Sales Trend", "orange")
colored_title("🟡 Product Sales Summary", "gold")
colored_title("🟢 Sales Data Table", "green")
colored_title("🔵 Sales by Product Category", "blue")

#   BAR CHART = region Sales

colored_title("🟣 Region-wise Sales", "purple")
region_sales = (
    filtered
    .groupby("Region")["Total Sales"]
    .sum()
    .reset_index()
)

bar_fig = px.bar(
    region_sales,
    x="Region",
    y="Total Sales",
    text=region_sales["Total Sales"].apply(lambda x: f"₹{x:,.0f}")
)

# ✅ Add ₹ to Y-axis
bar_fig.update_layout(
    yaxis_title="Total Sales (₹)",
    xaxis_title="Region",
    yaxis=dict(
        tickprefix="₹",
        tickformat=",."
    )
)

# Hover format
bar_fig.update_traces(
    hovertemplate="Region: %{x}<br>Sales: ₹%{y:,.0f}<extra></extra>",
    textposition="outside"
)

st.plotly_chart(bar_fig, use_container_width=True)
# LINE CHART - Yearly Sales
colored_title(" 📈 Monthly Sales Trend", "orange")
filtered = filtered.copy()
filtered["Month"] = filtered["Invoice Date"].dt.to_period("M").astype(str)

monthly_sales = (
    filtered
    .groupby("Month")["Total Sales"]
    .sum()
    .reset_index()
)

monthly_sales = monthly_sales.sort_values("Month")

line_fig = px.line(
    monthly_sales,
    x="Month",
    y="Total Sales",
    markers=True,
    title="Monthly Sales Trend",
    labels={
        "Month": "Month",
        "Total Sales": "Total Sales (₹)"
    }
)

# ₹ formatting on Y-axis
line_fig.update_layout(
    yaxis=dict(
        tickprefix="₹",
        tickformat=",."
    )
)

# Add labels on each point
line_fig.update_traces(
    line_shape="spline",
    mode="lines+markers+text",   # important for showing labels
    text=monthly_sales["Total Sales"].apply(lambda x: f"₹{x:,.0f}"),
    textposition="top center",
    hovertemplate="Month: %{x}<br>Sales: ₹%{y:,.0f}<extra></extra>"
)

st.plotly_chart(line_fig, use_container_width=True)
#STACKED BAR - Product Sales by Mont
colored_title("🟡 Product Sales Summary", "gold")
prod_month = (
    filtered
    .groupby(["Month", "Product Category"])["Total Sales"]
    .sum()
    .reset_index()
)

stack_fig = px.bar(
    prod_month,
    x="Month",
    y="Total Sales",
    color="Product Category",
    text=prod_month["Total Sales"].apply(lambda x: f"₹{x:,.0f}"),
    barmode="stack"
)

stack_fig.update_layout(
    yaxis_title="Total Sales (₹)",
    xaxis_title="Month",
    yaxis=dict(
        tickprefix="₹",
        tickformat=",."
    )
)

stack_fig.update_traces(
    hovertemplate="Month: %{x}<br>Sales: ₹%{y:,.0f}<extra></extra>",
    textposition="inside"
)

st.plotly_chart(stack_fig, use_container_width=True)

# DATA TABLE
colored_title("🟢 Sales Data Table", "green")
st.dataframe(filtered)
# DOWNLOAD OPTION
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# PIE CHART - Product Category Sales
colored_title("🔵 Sales by Product Category", "blue")
pie_data = (
    filtered
    .groupby("Product Category")["Total Sales"]
    .sum()
    .reset_index()
)

pie_fig = px.pie(
    pie_data,
    names="Product Category",
    values="Total Sales",
    hole=0.4
)

# ✅ Show ₹ instead of %  
pie_fig.update_traces(
    texttemplate="₹%{value:,.0f}<br>(%{percent})",  
    hovertemplate="%{label}: ₹%{value:,.0f} (%{percent})<extra></extra>"
)

st.plotly_chart(pie_fig, use_container_width=True)
#background color
st.markdown("""
<style>
.stApp{
    background-color: #e74c3c;
    color: white;
}
</style>
""",unsafe_allow_html=True)


