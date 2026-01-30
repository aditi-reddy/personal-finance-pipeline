# Personal Finance Data Pipeline
### End-to-End Data Engineering Project

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📊 Project Overview

Building a production-grade personal finance analytics platform that demonstrates end-to-end data engineering skills. This project showcases data pipeline development, cloud architecture, data quality frameworks, and analytics visualization.

**Business Problem:** Individuals need a comprehensive view of their financial health, spending patterns, and budget tracking to make informed financial decisions.

**Solution:** A scalable data pipeline that ingests, processes, validates, and analyzes financial transaction data to deliver actionable insights through interactive dashboards.

---

## 🎯 Project Goals

- Build realistic financial transaction datasets
- Design and implement ETL/ELT pipelines
- Establish data quality frameworks
- Deploy cloud-based data infrastructure (AWS)
- Create data warehouse with optimized schemas
- Develop interactive analytics dashboards
- Implement data security best practices

---

## 🛠️ Tech Stack

**Programming & Data Processing:**
- Python 3.12
- Pandas (data manipulation)
- PySpark (distributed processing)
- SQL (data querying)

**Cloud Platform:**
- AWS S3 (data lake storage)
- AWS Glue (ETL processing)
- AWS Lambda (automation)

**Database:**
- PostgreSQL 15 (data warehouse)
- pgAdmin 4 (database administration)

**Data Quality & Testing:**
- Great Expectations
- Pandas validation
- Unit testing (pytest)

**Visualization:**
- Tableau Public
- Python (matplotlib, seaborn)

**Version Control:**
- Git & GitHub

---

## 📁 Project Structure
```
personal-finance-pipeline/
│
├── README.md
├── data/
│   ├── transactions.csv              # Original generated data
│   └── silver_transactions.parquet   # Processed data from ETL
│
├── data_generation/
│   └── generate_transactions.py      # Synthetic data generator
│
├── data_transformation/
│   └── bronze_to_silver.py           # PySpark ETL script
│
├── data_quality/
│   ├── setup_gx.py                   # Great Expectations setup
│   ├── download_silver_data.py       # Download data from S3
│   └── create_expectations.py        # Quality validation script
│
├── sql/                              # ⭐ NEW
│   ├── create_schema.sql             # Database schema creation
│   └── load_data_to_postgres.py      # Data loading script
│
├── dashboards/                       # Coming soon
└── docs/                             # Coming soon
```

---

## 🚀 Current Progress

### ✅ Phase 1: Data Generation (Completed - Dec 2024)

**What I Built:**
- Synthetic transaction data generator using Python
- Realistic financial data across 10 spending categories
- 1,000+ transaction records with proper data types
- Date ranges spanning 2 years (2023-2024)

**Key Features:**
- **Categories:** Groceries, Restaurants, Gas, Utilities, Rent, Entertainment, Shopping, Healthcare, Transportation, Subscriptions
- **Data Fields:** Transaction ID, Date, Time, Merchant, Category, Amount, Payment Method, Status
- **Validation:** Proper date formats, realistic amount ranges, weighted category distribution

**Statistics Generated:**
- Total Transactions: 1,000
- Total Amount: $160,934.34
- Average Transaction: $160.93
- Date Range: Jan 2023 - Dec 2024

**Technical Implementation:**
- Used Python's `random` library for data generation
- Implemented weighted sampling for realistic category distribution
- Applied data sorting and CSV export functionality
- Added summary statistics calculation

---

### ✅ Phase 2: AWS Infrastructure Setup (Completed - Dec 2024)

**What I Built:**
- AWS Free Tier account with billing alerts configured
- Medallion architecture: 3 S3 buckets (Bronze/Silver/Gold layers)
- Uploaded 1,000 transaction records (70.1 KB) to cloud storage
- Implemented Hive-style date partitioning (year=YYYY/month=MM)
- Created IAM user with least-privilege access policies

**Key Features:**
- **S3 Buckets:** 
  - Bronze: aditi-finance-bronze-raw-2025 (raw data layer)
  - Silver: aditi-finance-silver-processed-2025 (processed data)
  - Gold: aditi-finance-gold-analytics-2025 (analytics-ready)
- **Data Partitioning:** year=2023/month=01/ structure for efficient queries
- **Security:** IAM policies, S3 encryption at rest, no public access
- **Cost Management:** Zero spend budget alerts, Free Tier monitoring

**Technical Implementation:**
- Configured S3 versioning for data recovery
- Enabled server-side encryption (SSE-S3)
- Created IAM user with S3FullAccess and CloudWatchReadOnly policies
- Implemented industry-standard medallion data lake architecture

**AWS Architecture:**
```
Local CSV → S3 Bronze (Raw) → S3 Silver (Processed) → S3 Gold (Analytics)
              ↓                    ↓                        ↓
          Partition by         ETL Processing         Ready for BI
          year/month          (Completed)              (Completed)
```

**Cost:** $0.00 (within Free Tier limits)

---

### ✅ Phase 3: ETL Pipeline Development (Completed - Jan 2026)

**What I Built:**
- AWS Glue ETL job using PySpark
- Data cleaning and validation pipeline
- Bronze → Silver layer transformation
- Automated data quality checks
- Parquet file format with compression

**Key Features:**
- **Data Cleaning:**
  - Removed duplicate transactions based on transaction_id
  - Handled missing values in critical fields
  - Fixed data type issues (amount to double, date to date type)
  - Validated amount ranges (removed amounts ≤ $0)
  
- **Data Validation:**
  - Category whitelist validation (10 allowed categories)
  - Payment method verification (4 allowed methods)
  - Date format standardization (yyyy-MM-dd)
  - Removed invalid/corrupted records

- **Data Enrichment:**
  - Added `day_of_week` column (1-7)
  - Added `month_name` column (January, February, etc.)
  - Added `year` and `month` columns for partitioning
  - Added `is_weekend` flag (boolean)
  - Standardized merchant names (lowercase, trimmed)

- **Technical Implementation:**
  - PySpark DataFrame transformations
  - Parquet file format (columnar, compressed) - 80% smaller than CSV
  - Partitioned by year/month for query optimization
  - AWS Glue Data Catalog integration
  - IAM role with Glue, S3, and CloudWatch permissions

**Data Quality:**
- Input: 1,000 records (Bronze layer, CSV format)
- Output: ~995-1000 records (Silver layer, Parquet format)
- Quality rate: 99.5%+
- Processing time: ~1-2 minutes
- File size reduction: 70 KB → ~12 KB (83% compression)

**Cost:** ~$0.10 per ETL job run

---

### ✅ Phase 4: Data Quality Framework (Completed - Jan 2026)

**What I Built:**
- Automated data quality validation framework
- 10+ quality checks covering completeness, uniqueness, validity, and statistics
- Python-based validation scripts with detailed reporting
- Data quality scoring system (0-100%)

**Key Features:**
- **Completeness Checks:**
  - Validated all required fields (transaction_id, date, merchant, amount)
  - Zero null values in critical columns
  
- **Uniqueness Checks:**
  - Transaction ID uniqueness validation
  - Zero duplicate records detected

- **Validity Checks:**
  - Amount range validation ($0.01 - $10,000)
  - Category whitelist (10 allowed categories)
  - Payment method validation (4 allowed methods)
  - All records passed validation

- **Statistical Checks:**
  - Average transaction: $162.44
  - Amount range: $5.73 - $1,819.03
  - Row count validation: 42 records
  - Category distribution analysis

**Technical Implementation:**
- Great Expectations framework setup
- Pandas-based data validation
- Automated quality scoring algorithm
- Category distribution analysis
- Null value detection
- Duplicate identification
- AWS CLI integration for S3 data access

**Data Quality Results:**
- **Quality Score: 100.00%**
- Records validated: 42
- Issues found: 0
- Clean records: 42 (100%)
- All validation checks: PASSED ✅

**Category Breakdown:**
- Groceries: 10 transactions
- Restaurants: 7 transactions
- Subscriptions: 6 transactions
- Entertainment: 5 transactions
- Transportation: 4 transactions
- Shopping: 4 transactions
- Gas: 3 transactions
- Rent: 2 transactions
- Healthcare: 1 transaction

**Cost:** $0.00 (runs locally)

---

### ✅ Phase 5-6: Data Warehouse Implementation (Completed - Jan 2026)

**What I Built:**
- PostgreSQL data warehouse with star schema design
- 5 tables: 1 fact table + 4 dimension tables
- Automated data loading pipeline from S3 to PostgreSQL
- Performance optimization with indexes
- Reusable views for common queries

**Key Features:**
- **Star Schema Architecture:**
  + Fact Table: `fact_transactions` (central transaction data)
  + Dimension Tables: `dim_date`, `dim_merchant`, `dim_category`, `dim_payment`
  + Foreign key relationships for data integrity
  + Optimized for analytical queries

- **Data Warehouse Statistics:**
  + Total Transactions: 42
  + Total Amount Spent: $6822.35
  + Average Transaction: $162.44
  + Date Range: 2023-01-01 - 2023-01-30
  + Unique Merchants: 26
  + Categories: 10
  + Payment Methods: 4

- **Performance Optimization:**
  + 10+ indexes on frequently queried columns
  + Composite indexes for complex queries
  + Views for common analytical patterns
  + Query execution under 100ms

**Technical Implementation:**
- PostgreSQL 15 database engine
- Python ETL script using psycopg2
- Automated dimension table population
- Foreign key constraint enforcement
- Transaction-based data loading

**Database Schema:**
```
fact_transactions (Fact Table)
├── transaction_key (PK)
├── transaction_id (Unique)
├── transaction_date (FK → dim_date)
├── merchant_key (FK → dim_merchant)
├── category_key (FK → dim_category)
├── payment_key (FK → dim_payment)
├── amount (DECIMAL)
└── status (VARCHAR)

dim_date (Dimension)
├── date_key (PK)
├── year, month, quarter
├── day_of_week, day_name
└── is_weekend (Boolean)

dim_merchant (Dimension)
├── merchant_key (PK)
├── merchant_name (Unique)
└── merchant_type

dim_category (Dimension)
├── category_key (PK)
├── category_name (Unique)
└── category_type

dim_payment (Dimension)
├── payment_key (PK)
├── payment_method (Unique)
└── payment_type
```

**SQL Capabilities:**
- Complex multi-table joins across star schema
- Aggregations by category, merchant, time period
- Window functions for running totals and rankings
- Percentage calculations and trend analysis
- Date-based filtering and grouping

**Cost:** $0.00 (local PostgreSQL installation)

---

## 📈 Next Steps

### Phase 7-8: SQL Analytics (In Progress)
- Write complex analytical queries
- Create aggregate tables and materialized views
- Build reporting queries for Tableau
- Implement advanced SQL techniques (window functions, CTEs)

### Phase 9: Pipeline Orchestration
- Automate entire workflow with Apache Airflow
- Schedule data refreshes
- Add monitoring and alerting

### Phase 10: Tableau Dashboards
- Build interactive visualizations
- Create spending analytics dashboard
- Implement budget tracking views

### Phase 11-12: Web Application
- Build React frontend
- Create interactive UI
- Deploy final product

---

## 💡 Key Learnings

### Week 1 Learnings:
- **Data Generation:** Understanding how to create realistic synthetic data while maintaining proper distributions
- **Python Best Practices:** Writing clean, documented, modular code
- **Git Workflow:** Setting up version control and pushing code to GitHub
- **Data Quality:** Ensuring generated data follows business rules and constraints

### Week 2 Learnings:
- **Cloud Architecture:** Medallion architecture (Bronze/Silver/Gold) for data lakes
- **AWS S3:** Object storage, versioning, encryption, and partitioning strategies
- **IAM Security:** Least-privilege access, role-based permissions
- **Cost Management:** Free Tier limits, billing alerts, resource optimization

### Week 3 Learnings:
- **ETL Fundamentals:** Extract, Transform, Load patterns and best practices
- **PySpark:** Distributed data processing with DataFrames and transformations
- **AWS Glue:** Managed ETL service, Data Catalog, and job orchestration
- **Data Formats:** CSV vs Parquet - columnar storage and compression benefits
- **Data Quality:** Validation rules, null handling, duplicate removal

### Week 4 Learnings:
- **Data Quality Framework:** Building automated validation systems
- **Great Expectations:** Industry-standard data quality tool
- **Quality Dimensions:** Completeness, uniqueness, validity, consistency
- **Validation Automation:** Running checks on every data pipeline execution
- **Quality Scoring:** Quantifying data health with metrics

### Week 5-6 Learnings:
- **Data Warehouse Design:** Star schema vs snowflake schema, dimensional modeling
- **PostgreSQL Administration:** Database creation, user management, security
- **ETL to Database:** Loading data from files into relational databases
- **SQL Optimization:** Indexes, query execution plans, performance tuning
- **Foreign Keys:** Data integrity, referential constraints
- **Normalization:** Dimension tables for efficient storage
- **Star Schema Benefits:** Fast queries, intuitive structure, business-friendly

---

## 🎓 Skills Demonstrated

- [x] Python Programming
- [x] Data Generation & Simulation
- [x] Git Version Control
- [x] AWS Cloud Services (S3, IAM, Glue)
- [x] ETL Pipeline Development
- [x] PySpark & Distributed Processing
- [x] Data Lake Architecture
- [x] Data Quality Engineering
- [x] Great Expectations Framework
- [x] AWS CLI Configuration
- [x] SQL & Data Modeling
- [x] Data Warehousing (PostgreSQL)
- [x] Database Administration
- [ ] Data Visualization (Tableau)
- [ ] Web Development (React)

---

## 📊 Sample Data

**Bronze Layer (CSV):**
```csv
transaction_id,date,time,merchant,category,amount,payment_method,status
TXN000239,2023-01-01,05:11,Walmart,Groceries,57.57,Debit Card,Posted
TXN000957,2023-01-02,21:10,Public Transit,Transportation,28.98,Debit Card,Posted
```

**Silver Layer (Parquet - enriched):**
```
transaction_id, date, merchant, category, amount, year, month, month_name, day_of_week, is_weekend
```

**Gold Layer (PostgreSQL - star schema):**
```sql
SELECT 
    f.transaction_id,
    d.month_name,
    m.merchant_name,
    c.category_name,
    p.payment_method,
    f.amount
FROM fact_transactions f
JOIN dim_date d ON f.transaction_date = d.date_key
JOIN dim_merchant m ON f.merchant_key = m.merchant_key
JOIN dim_category c ON f.category_key = c.category_key
JOIN dim_payment p ON f.payment_key = p.payment_key;
```

---

## 🔧 How to Run

### Prerequisites
- Python 3.12+
- AWS Account with Glue access
- AWS CLI configured
- PostgreSQL 15+
- Git

### Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/aditi-reddy/personal-finance-pipeline.git
cd personal-finance-pipeline
```

2. **Generate transaction data:**
```bash
cd data_generation
python generate_transactions.py
```

3. **Run ETL pipeline:**
- Upload `data_transformation/bronze_to_silver.py` to S3
- Create AWS Glue job pointing to the script
- Configure IAM role with necessary permissions
- Run the job from AWS Glue console

4. **Run data quality checks:**
```bash
cd data_quality
python download_silver_data.py  # Download processed data
python create_expectations.py    # Run quality validation
```

5. **Set up data warehouse:**
```bash
# Install PostgreSQL and pgAdmin
# Create database
psql -U postgres -c "CREATE DATABASE personal_finance_warehouse;"

# Run schema creation
cd sql
psql -U postgres -d personal_finance_warehouse -f create_schema.sql

# Load data
python load_data_to_postgres.py
```

---

## 📝 Documentation

Detailed documentation for each phase:
- ✅ Data generation process
- ✅ AWS infrastructure setup
- ✅ ETL pipeline architecture
- ✅ Data quality framework
- ✅ Data warehouse design and implementation
- Coming: SQL analytics queries
- Coming: Dashboard development

---

## 🤝 Connect With Me

**Aditi Malla**
- 📧 Email: aditireddy205@gmail.com
- 💼 LinkedIn: [linkedin.com/in/aditi-reddy-275a70222](http://www.linkedin.com/in/aditi-reddy-275a70222)
- 🎓 MS Information Systems @ Central Michigan University

---

## 📌 Project Timeline

- **Week 1 (Dec 2024):** ✅ Data generation complete
- **Week 2 (Dec 2024):** ✅ AWS infrastructure setup complete
- **Week 3 (Jan 2026):** ✅ ETL pipeline development complete
- **Week 4 (Jan 2026):** ✅ Data quality framework complete
- **Week 5-6 (Jan 2026):** ✅ Data warehouse implementation complete
- **Week 7-8:** SQL analytics & queries
- **Week 9:** Pipeline orchestration
- **Week 10:** Tableau dashboards
- **Week 11-12:** React web application

---

## ⭐ Acknowledgments

This project is part of my portfolio to demonstrate data engineering capabilities for full-time opportunities. Special focus on fintech industry standards including data security, compliance considerations, and production-ready code.

---

## 📄 License

This project is open source and available under the MIT License.

---

**Status:** 🚧 Active Development | Last Updated: January 2026 | 50% Complete (6/12 weeks)