"""
Personal Finance Data Generator
This script creates realistic synthetic financial transaction data
Author: Aditi Malla
Date: December 2024
"""

import random
import csv
from datetime import datetime, timedelta

# ============================================
# CONFIGURATION - You can change these numbers
# ============================================
NUM_TRANSACTIONS = 1000  # How many transactions to generate
START_DATE = datetime(2023, 1, 1)  # When transactions start
END_DATE = datetime(2024, 12, 13)  # When transactions end

# ============================================
# TRANSACTION CATEGORIES
# ============================================
CATEGORIES = {
    'Groceries': {'min': 20, 'max': 150, 'frequency': 0.20},
    'Restaurants': {'min': 15, 'max': 80, 'frequency': 0.15},
    'Gas': {'min': 30, 'max': 70, 'frequency': 0.10},
    'Utilities': {'min': 50, 'max': 200, 'frequency': 0.05},
    'Rent': {'min': 800, 'max': 2000, 'frequency': 0.05},
    'Entertainment': {'min': 10, 'max': 100, 'frequency': 0.10},
    'Shopping': {'min': 25, 'max': 300, 'frequency': 0.15},
    'Healthcare': {'min': 30, 'max': 500, 'frequency': 0.05},
    'Transportation': {'min': 5, 'max': 50, 'frequency': 0.08},
    'Subscriptions': {'min': 5, 'max': 30, 'frequency': 0.07}
}

# Merchant names for each category
MERCHANTS = {
    'Groceries': ['Walmart', 'Kroger', 'Whole Foods', 'Trader Joes', 'Costco'],
    'Restaurants': ['Chipotle', 'Starbucks', 'McDonalds', 'Subway', 'Panera'],
    'Gas': ['Shell', 'BP', 'Exxon', 'Chevron', 'Marathon'],
    'Utilities': ['Electric Company', 'Water Dept', 'Internet Provider', 'Gas Company'],
    'Rent': ['Property Management', 'Landlord'],
    'Entertainment': ['Netflix', 'Spotify', 'AMC Theaters', 'Amazon Prime'],
    'Shopping': ['Amazon', 'Target', 'Best Buy', 'Macys', 'Nike'],
    'Healthcare': ['CVS Pharmacy', 'Walgreens', 'Medical Center', 'Dentist Office'],
    'Transportation': ['Uber', 'Lyft', 'Public Transit', 'Parking'],
    'Subscriptions': ['Netflix', 'Spotify', 'Gym Membership', 'Adobe', 'Microsoft 365']
}

# ============================================
# GENERATE RANDOM DATE
# ============================================
def random_date(start, end):
    """Generate a random date between start and end"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

# ============================================
# GENERATE ONE TRANSACTION
# ============================================
def generate_transaction(transaction_id):
    """Generate a single transaction record"""
    
    # Randomly pick a category based on frequency
    category = random.choices(
        list(CATEGORIES.keys()),
        weights=[CATEGORIES[c]['frequency'] for c in CATEGORIES.keys()]
    )[0]
    
    # Get merchant and amount based on category
    merchant = random.choice(MERCHANTS[category])
    amount = round(random.uniform(
        CATEGORIES[category]['min'],
        CATEGORIES[category]['max']
    ), 2)
    
    # Generate random date and time
    transaction_date = random_date(START_DATE, END_DATE)
    transaction_time = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}"
    
    # Payment methods
    payment_method = random.choice(['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet'])
    
    # Transaction status (most are posted, some pending)
    status = random.choices(['Posted', 'Pending'], weights=[0.95, 0.05])[0]
    
    return {
        'transaction_id': f'TXN{transaction_id:06d}',
        'date': transaction_date.strftime('%Y-%m-%d'),
        'time': transaction_time,
        'merchant': merchant,
        'category': category,
        'amount': amount,
        'payment_method': payment_method,
        'status': status
    }

# ============================================
# MAIN FUNCTION
# ============================================
def main():
    """Main function to generate all transactions and save to CSV"""
    
    print("=" * 60)
    print("PERSONAL FINANCE DATA GENERATOR")
    print("=" * 60)
    print(f"Generating {NUM_TRANSACTIONS} transactions...")
    print(f"Date range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
    print()
    
    # Generate all transactions
    transactions = []
    for i in range(1, NUM_TRANSACTIONS + 1):
        transaction = generate_transaction(i)
        transactions.append(transaction)
        
        # Print progress every 100 transactions
        if i % 100 == 0:
            print(f"Generated {i}/{NUM_TRANSACTIONS} transactions...")
    
    # Sort transactions by date
    transactions.sort(key=lambda x: x['date'])
    
    # Save to CSV file
    output_file = '../data/transactions.csv'
    
    print()
    print("Saving to CSV file...")
    
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['transaction_id', 'date', 'time', 'merchant', 
                     'category', 'amount', 'payment_method', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(transactions)
    
    print(f"✅ Successfully created {output_file}")
    print()
    
    # Print summary statistics
    print("=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    
    total_amount = sum(t['amount'] for t in transactions)
    avg_transaction = total_amount / len(transactions)
    
    print(f"Total transactions: {len(transactions)}")
    print(f"Total amount: ${total_amount:,.2f}")
    print(f"Average transaction: ${avg_transaction:.2f}")
    print()
    
    # Transactions by category
    print("Transactions by Category:")
    category_counts = {}
    category_amounts = {}
    
    for t in transactions:
        cat = t['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
        category_amounts[cat] = category_amounts.get(cat, 0) + t['amount']
    
    for category in sorted(category_counts.keys()):
        count = category_counts[category]
        amount = category_amounts[category]
        print(f"  {category:20s}: {count:4d} transactions | ${amount:10,.2f}")
    
    print()
    print("=" * 60)
    print("Data generation complete! 🎉")
    print("=" * 60)

# ============================================
# RUN THE SCRIPT
# ============================================
if __name__ == "__main__":
    main()