"""
Load data from Parquet to PostgreSQL
"""

print("=" * 70)
print("LOADING DATA TO POSTGRESQL")
print("=" * 70)

import pandas as pd
import psycopg2
from datetime import datetime

# Database connection
print("\n🔌 Connecting to PostgreSQL...")
try:
    conn = psycopg2.connect(
        host="localhost",
        database="personal_finance_warehouse",
        user="postgres",
        password=""  # Leave blank if no password
    )
    cur = conn.cursor()
    print("✅ Connected to PostgreSQL")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)

# Load data from Parquet
print("\n📥 Loading data from Parquet...")
df = pd.read_parquet('../data/silver_transactions.parquet')
print(f"✅ Loaded {len(df)} records")

# ============================================
# 1. LOAD DIM_DATE
# ============================================
print("\n1️⃣  Loading dim_date...")

unique_dates = df['date'].unique()
date_data = []

for date in unique_dates:
    dt = pd.to_datetime(date)
    date_data.append({
        'date_key': dt.date(),
        'year': dt.year,
        'month': dt.month,
        'month_name': dt.strftime('%B'),
        'quarter': (dt.month - 1) // 3 + 1,
        'day_of_week': dt.dayofweek + 1,
        'day_name': dt.strftime('%A'),
        'is_weekend': dt.dayofweek >= 5
    })

for d in date_data:
    cur.execute("""
        INSERT INTO dim_date (date_key, year, month, month_name, quarter, day_of_week, day_name, is_weekend)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (date_key) DO NOTHING
    """, (d['date_key'], d['year'], d['month'], d['month_name'], 
          d['quarter'], d['day_of_week'], d['day_name'], d['is_weekend']))

conn.commit()
print(f"   ✅ Loaded {len(date_data)} dates")

# ============================================
# 2. LOAD DIM_CATEGORY
# ============================================
print("\n2️⃣  Loading dim_category...")

category_mapping = {
    'Groceries': 'Essential',
    'Utilities': 'Essential',
    'Healthcare': 'Essential',
    'Rent': 'Essential',
    'Gas': 'Essential',
    'Restaurants': 'Discretionary',
    'Entertainment': 'Discretionary',
    'Shopping': 'Discretionary',
    'Subscriptions': 'Discretionary',
    'Transportation': 'Essential'
}

category_keys = {}
for category, cat_type in category_mapping.items():
    cur.execute("""
        INSERT INTO dim_category (category_name, category_type)
        VALUES (%s, %s)
        RETURNING category_key
    """, (category, cat_type))
    category_keys[category] = cur.fetchone()[0]

conn.commit()
print(f"   ✅ Loaded {len(category_keys)} categories")

# ============================================
# 3. LOAD DIM_MERCHANT
# ============================================
print("\n3️⃣  Loading dim_merchant...")

unique_merchants = df['merchant'].unique()
merchant_keys = {}

for merchant in unique_merchants:
    cur.execute("""
        INSERT INTO dim_merchant (merchant_name, merchant_type)
        VALUES (%s, %s)
        RETURNING merchant_key
    """, (merchant.title(), 'Physical'))
    merchant_keys[merchant] = cur.fetchone()[0]

conn.commit()
print(f"   ✅ Loaded {len(merchant_keys)} merchants")

# ============================================
# 4. LOAD DIM_PAYMENT
# ============================================
print("\n4️⃣  Loading dim_payment...")

payment_mapping = {
    'Credit Card': 'Digital',
    'Debit Card': 'Digital',
    'Cash': 'Physical',
    'Digital Wallet': 'Digital'
}

payment_keys = {}
for method, p_type in payment_mapping.items():
    cur.execute("""
        INSERT INTO dim_payment (payment_method, payment_type)
        VALUES (%s, %s)
        RETURNING payment_key
    """, (method, p_type))
    payment_keys[method] = cur.fetchone()[0]

conn.commit()
print(f"   ✅ Loaded {len(payment_keys)} payment methods")

# ============================================
# 5. LOAD FACT_TRANSACTIONS
# ============================================
print("\n5️⃣  Loading fact_transactions...")

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO fact_transactions 
        (transaction_id, transaction_date, merchant_key, category_key, payment_key, amount, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row['transaction_id'],
        pd.to_datetime(row['date']).date(),
        merchant_keys[row['merchant']],
        category_keys[row['category']],
        payment_keys[row['payment_method']],
        float(row['amount']),
        row['status']
    ))

conn.commit()
print(f"   ✅ Loaded {len(df)} transactions")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 70)
print("DATA LOAD COMPLETE!")
print("=" * 70)

# Verify counts
cur.execute("SELECT COUNT(*) FROM dim_date")
print(f"\ndim_date: {cur.fetchone()[0]} records")

cur.execute("SELECT COUNT(*) FROM dim_category")
print(f"dim_category: {cur.fetchone()[0]} records")

cur.execute("SELECT COUNT(*) FROM dim_merchant")
print(f"dim_merchant: {cur.fetchone()[0]} records")

cur.execute("SELECT COUNT(*) FROM dim_payment")
print(f"dim_payment: {cur.fetchone()[0]} records")

cur.execute("SELECT COUNT(*) FROM fact_transactions")
print(f"fact_transactions: {cur.fetchone()[0]} records")

print("\n" + "=" * 70)

# Close connection
cur.close()
conn.close()

print("✅ Connection closed")