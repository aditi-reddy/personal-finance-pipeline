"""
Personal Finance Dashboard
Built with Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 💰 Personal Finance")
    st.markdown("#### Analytics Dashboard")
    st.markdown("---")
    
    st.info("""
    **📊 Project Info**
    
    12-week data engineering project completed in 10 weeks!
    
    **Built with:**
    - Python 3.12
    - Streamlit
    - PostgreSQL 15
    - Apache Airflow
    - Plotly
    - AWS S3
    """)
    
    st.success("✅ Connected to database")
    
    st.markdown("---")
    st.caption("Built by Aditi Malla")
    st.caption("MS Information Systems @ CMU")
    st.caption("v1.0.0 • Week 10 Project")

# Database connection configuration
PG_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'personal_finance_warehouse',
    'user': 'aditireddy',
    'password': ''
}

# Connect to database
@st.cache_resource
def get_database_connection():
    """Create database connection with caching"""
    return psycopg2.connect(**PG_CONFIG)

# Load data with caching
@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_data(query):
    """Load data from PostgreSQL"""
    conn = get_database_connection()
    df = pd.read_sql(query, conn)
    return df

# Main dashboard
def main():
    # Title
    st.title("💰 Personal Finance Analytics")
    st.markdown("### Executive Summary Dashboard")
    st.markdown("---")
    
    # Load summary data
    summary_query = """
    SELECT 
        COUNT(*) as total_transactions,
        SUM(amount) as total_spent,
        AVG(amount) as avg_transaction,
        COUNT(DISTINCT category) as total_categories
    FROM staging_transactions
    """
    summary = load_data(summary_query)
    
    # KPI Cards in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💵 Total Spending",
            value=f"${summary['total_spent'][0]:,.2f}",
            delta="All time"
        )
    
    with col2:
        st.metric(
            label="📊 Avg Transaction",
            value=f"${summary['avg_transaction'][0]:,.2f}",
            delta=f"{summary['total_transactions'][0]} transactions"
        )
    
    with col3:
        st.metric(
            label="🏷️ Categories",
            value=f"{summary['total_categories'][0]}",
            delta="Active"
        )
    
    with col4:
        st.metric(
            label="📅 Transactions",
            value=f"{summary['total_transactions'][0]:,}",
            delta="Total"
        )
    
    st.markdown("---")
    
    # Charts in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Category spending chart
        st.subheader("📊 Spending by Category")
        
        category_query = """
        SELECT 
            category,
            SUM(amount) as total_spent,
            COUNT(*) as transaction_count
        FROM staging_transactions
        GROUP BY category
        ORDER BY total_spent DESC
        """
        df_category = load_data(category_query)
        
        fig = px.bar(
            df_category,
            x='total_spent',
            y='category',
            orientation='h',
            title='Total Spending by Category',
            labels={'total_spent': 'Amount ($)', 'category': 'Category'},
            color='total_spent',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Category pie chart
        st.subheader("🥧 Category Breakdown")
        
        fig_pie = px.pie(
            df_category,
            values='total_spent',
            names='category',
            title='Spending Distribution',
            hole=0.4  # Donut chart
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Monthly trend
    st.markdown("---")
    st.subheader("📈 Monthly Spending Trend")
    
    monthly_query = """
    SELECT 
        year,
        month,
        SUM(amount) as total_spent,
        COUNT(*) as transaction_count
    FROM staging_transactions
    GROUP BY year, month
    ORDER BY year, month
    """
    df_monthly = load_data(monthly_query)
    df_monthly['month_year'] = df_monthly['year'].astype(str) + '-' + df_monthly['month'].astype(str).str.zfill(2)
    
    fig_trend = px.line(
        df_monthly,
        x='month_year',
        y='total_spent',
        title='Spending Over Time',
        labels={'month_year': 'Month', 'total_spent': 'Amount ($)'},
        markers=True
    )
    fig_trend.update_layout(height=300)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Top merchants
    st.markdown("---")
    st.subheader("🏪 Top 10 Merchants")
    
    merchant_query = """
    SELECT 
        merchant,
        SUM(amount) as total_spent,
        COUNT(*) as visit_count
    FROM staging_transactions
    GROUP BY merchant
    ORDER BY total_spent DESC
    LIMIT 10
    """
    df_merchants = load_data(merchant_query)
    
    fig_merchants = px.bar(
        df_merchants,
        x='total_spent',
        y='merchant',
        orientation='h',
        title='Top Merchants by Spending',
        labels={'total_spent': 'Amount ($)', 'merchant': 'Merchant'},
        color='visit_count',
        color_continuous_scale='Blues'
    )
    fig_merchants.update_layout(height=400)
    st.plotly_chart(fig_merchants, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.caption("📊 Data refreshed every 10 minutes • Built with Streamlit")

if __name__ == "__main__":
    main()
