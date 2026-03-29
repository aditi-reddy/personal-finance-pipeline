"""
Time-based Analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2

st.set_page_config(page_title="Time Analysis", page_icon="📅", layout="wide")

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

st.title("📅 Time Analysis")
st.markdown("### Understand spending patterns over time")
st.markdown("---")

# Day of week analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Spending by Day of Week")
    
    dow_query = """
    SELECT 
        day_of_week,
        CASE day_of_week
            WHEN 0 THEN 'Monday'
            WHEN 1 THEN 'Tuesday'
            WHEN 2 THEN 'Wednesday'
            WHEN 3 THEN 'Thursday'
            WHEN 4 THEN 'Friday'
            WHEN 5 THEN 'Saturday'
            WHEN 6 THEN 'Sunday'
        END as day_name,
        SUM(amount) as total_spent,
        AVG(amount) as avg_spent,
        COUNT(*) as transaction_count
    FROM staging_transactions
    GROUP BY day_of_week
    ORDER BY day_of_week
    """
    df_dow = load_data(dow_query)
    
    fig = px.bar(
        df_dow,
        x='day_name',
        y='total_spent',
        color='avg_spent',
        color_continuous_scale='Blues',
        labels={'day_name': 'Day', 'total_spent': 'Total Spent ($)', 'avg_spent': 'Avg Transaction ($)'}
    )
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏖️ Weekend vs Weekday")
    
    weekend_query = """
    SELECT 
        CASE 
            WHEN day_of_week IN (5, 6) THEN 'Weekend'
            ELSE 'Weekday'
        END as period,
        SUM(amount) as total_spent,
        COUNT(*) as transaction_count,
        AVG(amount) as avg_amount
    FROM staging_transactions
    GROUP BY period
    """
    df_weekend = load_data(weekend_query)
    
    fig_pie = px.pie(
        df_weekend,
        values='total_spent',
        names='period',
        hole=0.4,
        color_discrete_map={'Weekend': '#FF6B6B', 'Weekday': '#4ECDC4'}
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

# Monthly trends
st.markdown("---")
st.subheader("📈 Cumulative Spending Over Time")

monthly_query = """
SELECT 
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as cumulative_spent
FROM staging_transactions
ORDER BY date
"""
df_cumulative = load_data(monthly_query)

fig_cumulative = px.area(
    df_cumulative,
    x='date',
    y='cumulative_spent',
    labels={'date': 'Date', 'cumulative_spent': 'Cumulative Spending ($)'}
)
fig_cumulative.update_layout(height=400)
st.plotly_chart(fig_cumulative, use_container_width=True)

# Spending by month
st.markdown("---")
st.subheader("📊 Monthly Spending Breakdown")

monthly_breakdown_query = """
SELECT 
    year,
    month,
    SUM(amount) as total_spent,
    COUNT(*) as transaction_count
FROM staging_transactions
GROUP BY year, month
ORDER BY year, month
"""
df_monthly = load_data(monthly_breakdown_query)
df_monthly['month_year'] = df_monthly['year'].astype(str) + '-' + df_monthly['month'].astype(str).str.zfill(2)

fig_monthly = px.bar(
    df_monthly,
    x='month_year',
    y='total_spent',
    color='transaction_count',
    color_continuous_scale='Viridis',
    labels={'month_year': 'Month', 'total_spent': 'Total Spent ($)', 'transaction_count': 'Transactions'}
)
fig_monthly.update_layout(height=400)
st.plotly_chart(fig_monthly, use_container_width=True)

st.caption("📅 Time-based insights • Built with Streamlit")
