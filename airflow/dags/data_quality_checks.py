"""
Data Quality Checks Module
Comprehensive validation rules for transaction data
"""

import pandas as pd
from datetime import datetime, timedelta


class DataQualityValidator:
    """
    Validates transaction data quality
    """
    
    def __init__(self, df):
        self.df = df
        self.issues = []
        self.warnings = []
        self.metrics = {}
    
    def validate_schema(self):
        """Check if all required columns are present"""
        required_columns = [
            'transaction_id',
            'date',
            'merchant',
            'category',
            'amount',
            'payment_method'
        ]
        
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        
        if missing_columns:
            self.issues.append(f"Missing required columns: {', '.join(missing_columns)}")
            return False
        
        print(f"✅ Schema validation: All required columns present")
        return True
    
    def validate_data_types(self):
        """Check data types are correct"""
        checks_passed = True
        
        # Check transaction_id is string
        if self.df['transaction_id'].dtype != 'object':
            self.issues.append("transaction_id must be string type")
            checks_passed = False
        
        # Check amount is numeric
        if not pd.api.types.is_numeric_dtype(self.df['amount']):
            self.issues.append("amount must be numeric type")
            checks_passed = False
        
        # Try parsing dates
        try:
            pd.to_datetime(self.df['date'])
        except Exception as e:
            self.issues.append(f"date column has invalid dates: {str(e)}")
            checks_passed = False
        
        if checks_passed:
            print(f"✅ Data type validation: All types correct")
        
        return checks_passed
    
    def validate_nulls(self):
        """Check for null values in critical columns"""
        critical_columns = ['transaction_id', 'date', 'amount']
        
        for col in critical_columns:
            null_count = self.df[col].isnull().sum()
            if null_count > 0:
                self.issues.append(f"{col} has {null_count} null values")
        
        # Track nulls in non-critical columns as warnings
        for col in self.df.columns:
            if col not in critical_columns:
                null_count = self.df[col].isnull().sum()
                if null_count > 0:
                    self.warnings.append(f"{col} has {null_count} null values")
        
        if not self.issues:
            print(f"✅ Null check: No nulls in critical columns")
        
        return len(self.issues) == 0
    
    def validate_duplicates(self):
        """Check for duplicate transactions"""
        # Check for exact duplicates
        exact_duplicates = self.df.duplicated().sum()
        
        # Check for duplicate transaction_ids
        duplicate_ids = self.df['transaction_id'].duplicated().sum()
        
        if exact_duplicates > 0:
            self.warnings.append(f"Found {exact_duplicates} exact duplicate rows")
        
        if duplicate_ids > 0:
            self.issues.append(f"Found {duplicate_ids} duplicate transaction IDs")
            return False
        
        print(f"✅ Duplicate check: No duplicate transaction IDs")
        return True
    
    def validate_amount_range(self):
        """Check amounts are within reasonable ranges"""
        checks_passed = True
        
        # Check for negative amounts
        negative_count = (self.df['amount'] < 0).sum()
        if negative_count > 0:
            self.issues.append(f"Found {negative_count} negative amounts")
            checks_passed = False
        
        # Check for zero amounts
        zero_count = (self.df['amount'] == 0).sum()
        if zero_count > 0:
            self.warnings.append(f"Found {zero_count} zero amounts")
        
        # Check for unusually large amounts (> $10,000)
        large_count = (self.df['amount'] > 10000).sum()
        if large_count > 0:
            self.warnings.append(f"Found {large_count} transactions > $10,000")
        
        # Track metrics
        self.metrics['min_amount'] = float(self.df['amount'].min())
        self.metrics['max_amount'] = float(self.df['amount'].max())
        self.metrics['avg_amount'] = float(self.df['amount'].mean())
        
        if checks_passed:
            print(f"✅ Amount range check: All amounts valid")
        
        return checks_passed
    
    def validate_date_range(self):
        """Check dates are within reasonable ranges"""
        self.df['parsed_date'] = pd.to_datetime(self.df['date'])
        
        min_date = self.df['parsed_date'].min()
        max_date = self.df['parsed_date'].max()
        
        # Check for future dates
        today = pd.Timestamp.now()
        future_count = (self.df['parsed_date'] > today).sum()
        
        if future_count > 0:
            self.issues.append(f"Found {future_count} future dates")
            return False
        
        # Check for very old dates (> 10 years ago)
        ten_years_ago = today - pd.Timedelta(days=3650)
        old_count = (self.df['parsed_date'] < ten_years_ago).sum()
        
        if old_count > 0:
            self.warnings.append(f"Found {old_count} dates older than 10 years")
        
        # Track metrics
        self.metrics['earliest_date'] = str(min_date.date())
        self.metrics['latest_date'] = str(max_date.date())
        
        print(f"✅ Date range check: All dates valid")
        return True
    
    def validate_categories(self):
        """Check for valid categories"""
        valid_categories = [
            'Groceries', 'Dining', 'Transportation', 'Entertainment',
            'Shopping', 'Bills', 'Healthcare', 'Travel', 'Other'
        ]
        
        invalid_categories = self.df[~self.df['category'].isin(valid_categories)]['category'].unique()
        
        if len(invalid_categories) > 0:
            self.warnings.append(f"Found unexpected categories: {', '.join(invalid_categories)}")
        
        # Track category distribution
        self.metrics['category_counts'] = self.df['category'].value_counts().to_dict()
        
        print(f"✅ Category check: {len(self.df['category'].unique())} unique categories")
        return True
    
    def detect_anomalies(self):
        """Detect unusual patterns in data"""
        # Check for unusual spending patterns
        avg_amount = self.df['amount'].mean()
        std_amount = self.df['amount'].std()
        
        # Flag transactions > 3 standard deviations from mean
        threshold = avg_amount + (3 * std_amount)
        anomalies = self.df[self.df['amount'] > threshold]
        
        if len(anomalies) > 0:
            self.warnings.append(f"Found {len(anomalies)} statistical anomalies (amount > 3 std dev)")
        
        # Check for merchant anomalies (same merchant, widely different amounts)
        merchant_stats = self.df.groupby('merchant')['amount'].agg(['mean', 'std', 'count'])
        merchant_stats = merchant_stats[merchant_stats['count'] > 5]  # Only merchants with 5+ transactions
        
        anomaly_merchants = []
        for merchant, row in merchant_stats.iterrows():
            if row['std'] > row['mean']:  # High variance
                anomaly_merchants.append(merchant)
        
        if anomaly_merchants:
            self.warnings.append(f"Found {len(anomaly_merchants)} merchants with high amount variance")
        
        print(f"✅ Anomaly detection: {len(anomalies)} statistical outliers detected")
        return True
    
    def run_all_checks(self):
        """Run all validation checks"""
        print("\n" + "=" * 60)
        print("🔍 RUNNING DATA QUALITY CHECKS")
        print("=" * 60)
        
        checks = [
            ('Schema Validation', self.validate_schema),
            ('Data Type Validation', self.validate_data_types),
            ('Null Check', self.validate_nulls),
            ('Duplicate Check', self.validate_duplicates),
            ('Amount Range Check', self.validate_amount_range),
            ('Date Range Check', self.validate_date_range),
            ('Category Validation', self.validate_categories),
            ('Anomaly Detection', self.detect_anomalies),
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            try:
                passed = check_func()
                if not passed:
                    all_passed = False
            except Exception as e:
                self.issues.append(f"{check_name} failed with error: {str(e)}")
                all_passed = False
        
        # Print results
        print("\n" + "=" * 60)
        print("📊 QUALITY CHECK RESULTS")
        print("=" * 60)
        
        if self.issues:
            print(f"\n❌ CRITICAL ISSUES ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  - {issue}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.issues and not self.warnings:
            print("\n✅ ALL CHECKS PASSED - NO ISSUES FOUND!")
        
        print("\n📈 QUALITY METRICS:")
        for key, value in self.metrics.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    - {k}: {v}")
            else:
                print(f"  {key}: {value}")
        
        print("=" * 60 + "\n")
        
        return all_passed, self.issues, self.warnings, self.metrics