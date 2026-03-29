"""
Category Deep Dive Analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

st.set_page_config(page_title="Category Analysis", page_icon="📊", layout="wide")

# Database connection
PG_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'personal_finance_warehouse',
    'user': 'aditireddy',
    'password': ''
}

@st.cache_resource
def get_connection():
    return psycopg2.connect(**PG_CONFIG)

@st.cache_data(ttl=600)
def load_data(query):
    conn = get_connection()
    return pd.read_sql(query, conn)

# Page header
st.title("📊 Category Deep Dive")
st.markdown("### Analyze spending patterns by category")
st.markdown("---")

# Get all categories
categories_query = "SELECT DISTINCT category FROM staging_transactions ORDER BY category"
categories = load_data(categories_query)['category'].tolist()

# Category selector
selected_category = st.selectbox(
    "Select a category to analyze:",
    categories,
    index=0
)

st.markdown(f"### Analyzing: **{selected_category}**")

# Category metrics
col1, col2, col3, col4 = st.columns(4)

category_summary_query = f"""
SELECT 
    COUNT(*) as transaction_count,
    SUM(amount) as total_spent,
    AVG(amount) as avg_amount,
    MAX(amount) as max_amount
FROM staging_transactions
WHERE category = '{selected_category}'
"""
summary = load_data(category_summary_query)

with col1:
    st.metric("💵 Total Spent", f"${summary['total_spent'][0]:,.2f}")

with col2:
    st.metric("📊 Avg Amount", f"${summary['avg_amount'][0]:,.2f}")

with col3:
    st.metric("📈 Max Transaction", f"${summary['max_amount'][0]:,.2f}")

with col4:
    st.metric("🔢 Transactions", f"{summary['transaction_count'][0]:,}")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    # Top merchants in category
    st.subheader(f"🏪 Top Merchants - {selected_category}")
    
    merchant_query = f"""
    SELECT 
        merchant,
        SUM(amount) as total_spent,
        COUNT(*) as visit_count
    FROM staging_transactions
    WHERE category = '{selected_category}'
    GROUP BY merchant
    ORDER BY total_spent DESC
    LIMIT 10
    """
    df_merchants = load_data(merchant_query)
    
    fig = px.bar(
        df_merchants,
        x='total_spent',
        y='merchant',
        orientation='h',
        color='visit_count',
        color_continuous_scale='Viridis',
        labels={'total_spent': 'Amount ($)', 'merchant': 'Merchant', 'visit_count': 'Visits'}
    )
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Payment methods
    st.subheader(f"💳 Payment Methods - {selected_category}")
    
    payment_query = f"""
    SELECT 
        payment_method,
        SUM(amount) as total_spent,
        COUNT(*) as transaction_count
    FROM staging_transactions
    WHERE category = '{selected_category}'
    GROUP BY payment_method
    ORDER BY total_spent DESC
    """
    df_payment = load_data(payment_query)
    
    fig_pie = px.pie(
        df_payment,
        values='total_spent',
        names='payment_method',
        hole=0.4
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

# Monthly trend for category
st.markdown("---")
st.subheader(f"📈 Monthly Trend - {selected_category}")

trend_query = f"""
SELECT 
    year,
    month,
    SUM(amount) as total_spent,
    COUNT(*) as transaction_count
FROM staging_transactions
WHERE category = '{selected_category}'
GROUP BY year, month
ORDER BY year, month
"""
df_trend = load_data(trend_query)
df_trend['month_year'] = df_trend['year'].astype(str) + '-' + df_trend['month'].astype(str).str.zfill(2)

fig_trend = px.line(
    df_trend,
    x='month_year',
    y='total_spent',
    markers=True,
    labels={'month_year': 'Month', 'total_spent': 'Amount ($)'}
)
fig_trend.update_layout(height=300)
st.plotly_chart(fig_trend, use_container_width=True)

# Transaction details
st.markdown("---")
st.subheader(f"📋 Recent Transactions - {selected_category}")

transactions_query = f"""
SELECT 
    date,
    merchant,
    amount,
    payment_method
FROM staging_transactions
WHERE category = '{selected_category}'
ORDER BY date DESC
LIMIT 20
"""
df_transactions = load_data(transactions_query)

st.dataframe(
    df_transactions,
    use_container_width=True,
    hide_index=True
)

st.caption("📊 Interactive category analysis • Built with Streamlit")
