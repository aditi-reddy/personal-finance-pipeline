"""
Create Data Quality Checks - Simplified
"""

print("=" * 70)
print("DATA QUALITY VALIDATION")
print("=" * 70)

import pandas as pd

# Load data
print("\n📥 Loading data...")
df = pd.read_parquet('../data/silver_transactions.parquet')
print(f"✅ Loaded {len(df)} records")

# Manual quality checks
print("\n" + "=" * 70)
print("RUNNING QUALITY CHECKS")
print("=" * 70)

total_records = len(df)
issues = []

# 1. COMPLETENESS
print("\n1️⃣  Completeness Checks:")
null_transaction_ids = df['transaction_id'].isnull().sum()
null_dates = df['date'].isnull().sum()
null_merchants = df['merchant'].isnull().sum()
null_amounts = df['amount'].isnull().sum()

print(f"   Null transaction_ids: {null_transaction_ids}")
print(f"   Null dates: {null_dates}")
print(f"   Null merchants: {null_merchants}")
print(f"   Null amounts: {null_amounts}")

if null_transaction_ids > 0:
    issues.append(f"{null_transaction_ids} null transaction_ids")
if null_dates > 0:
    issues.append(f"{null_dates} null dates")
if null_merchants > 0:
    issues.append(f"{null_merchants} null merchants")
if null_amounts > 0:
    issues.append(f"{null_amounts} null amounts")

# 2. UNIQUENESS
print("\n2️⃣  Uniqueness Checks:")
unique_ids = df['transaction_id'].nunique()
duplicate_ids = total_records - unique_ids
print(f"   Unique transaction_ids: {unique_ids}")
print(f"   Duplicate transaction_ids: {duplicate_ids}")

if duplicate_ids > 0:
    issues.append(f"{duplicate_ids} duplicate transaction_ids")

# 3. VALIDITY
print("\n3️⃣  Validity Checks:")

# Amount range
invalid_amounts = df[(df['amount'] <= 0) | (df['amount'] > 10000)].shape[0]
print(f"   Invalid amounts (<=0 or >10000): {invalid_amounts}")
if invalid_amounts > 0:
    issues.append(f"{invalid_amounts} invalid amounts")

# Categories
allowed_categories = [
    'Groceries', 'Restaurants', 'Gas', 'Utilities', 'Rent',
    'Entertainment', 'Shopping', 'Healthcare', 'Transportation', 'Subscriptions'
]
invalid_categories = df[~df['category'].isin(allowed_categories)].shape[0]
print(f"   Invalid categories: {invalid_categories}")
if invalid_categories > 0:
    issues.append(f"{invalid_categories} invalid categories")

# Payment methods
allowed_payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet']
invalid_payment = df[~df['payment_method'].isin(allowed_payment_methods)].shape[0]
print(f"   Invalid payment methods: {invalid_payment}")
if invalid_payment > 0:
    issues.append(f"{invalid_payment} invalid payment methods")

# 4. STATISTICAL CHECKS
print("\n4️⃣  Statistical Checks:")
avg_amount = df['amount'].mean()
min_amount = df['amount'].min()
max_amount = df['amount'].max()

print(f"   Average amount: ${avg_amount:.2f}")
print(f"   Min amount: ${min_amount:.2f}")
print(f"   Max amount: ${max_amount:.2f}")
print(f"   Row count: {total_records}")

# CALCULATE QUALITY SCORE
total_issues = sum([
    null_transaction_ids, null_dates, null_merchants, null_amounts,
    duplicate_ids, invalid_amounts, invalid_categories, invalid_payment
])

quality_score = ((total_records - total_issues) / total_records) * 100 if total_records > 0 else 0

# RESULTS
print("\n" + "=" * 70)
print("QUALITY REPORT")
print("=" * 70)

print(f"\n📊 Total Records: {total_records}")
print(f"🔍 Issues Found: {total_issues}")
print(f"✅ Clean Records: {total_records - total_issues}")
print(f"📈 Quality Score: {quality_score:.2f}%")

if issues:
    print(f"\n⚠️  Issues Detected:")
    for issue in issues:
        print(f"   - {issue}")
else:
    print(f"\n🎉 NO ISSUES FOUND! Data quality is 100%!")

# Summary by category
print(f"\n📋 Transactions by Category:")
category_counts = df['category'].value_counts()
for category, count in category_counts.items():
    print(f"   {category:20s}: {count:3d} transactions")

print("\n" + "=" * 70)
print("VALIDATION COMPLETE!")
print("=" * 70)