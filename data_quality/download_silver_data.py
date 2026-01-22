"""
Download Silver Data from S3
"""

print("=" * 70)
print("DOWNLOADING DATA FROM S3")
print("=" * 70)

import boto3
import pandas as pd
from io import BytesIO
import os

# Configuration
BUCKET_NAME = 'aditi-finance-silver-processed-2025'
PREFIX = 'transactions/year=2023/month=1/'
OUTPUT_PATH = '../data/silver_transactions.parquet'

print(f"\nBucket: {BUCKET_NAME}")
print(f"Path: {PREFIX}")
print(f"\nConnecting to S3...")

# Initialize S3 client
try:
    s3 = boto3.client('s3', region_name='us-east-1')
    print("✅ Connected to S3")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# List objects
print(f"\nListing files...")

try:
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
    
    if 'Contents' not in response:
        print("❌ No files found!")
        exit(1)
    
    print(f"✅ Found {len(response['Contents'])} objects")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Download Parquet files
print("\nDownloading...")
dfs = []

for obj in response['Contents']:
    key = obj['Key']
    
    if key.endswith('.parquet'):
        print(f"  Reading: {key}")
        
        try:
            obj_response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
            df = pd.read_parquet(BytesIO(obj_response['Body'].read()))
            dfs.append(df)
        except Exception as e:
            print(f"  ❌ Error: {e}")

# Combine
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Save
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    combined_df.to_parquet(OUTPUT_PATH, index=False)
    
    print("\n" + "=" * 70)
    print("SUCCESS!")
    print("=" * 70)
    print(f"\n✅ Downloaded {len(combined_df)} records")
    print(f"✅ Saved to: {OUTPUT_PATH}")
    print(f"\n📊 Preview:")
    print(combined_df.head())
    print(f"\n📋 Columns: {list(combined_df.columns)}")
    
else:
    print("\n❌ No Parquet files found!")

print("\n" + "=" * 70)