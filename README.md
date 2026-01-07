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
- AWS Redshift (data warehouse)

**Data Quality & Testing:**
- Great Expectations
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
│   └── transactions.csv          # Generated transaction data
│
├── data_generation/
│   └── generate_transactions.py  # Synthetic data generator
│
├── data_transformation/
│   └── bronze_to_silver.py       # PySpark ETL script
│
├── data_quality/                 # Coming soon
├── sql/                          # Coming soon
├── dashboards/                   # Coming soon
└── docs/                         # Coming soon
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
          year/month          (Coming Week 3)         (Coming Week 6)
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

## 📈 Next Steps

### Phase 4: Data Quality Framework
- Set up Great Expectations
- Define expectation suites
- Create automated quality reports
- Implement data validation checks

### Phase 5: Data Warehouse
- Design star schema
- Set up Redshift cluster
- Optimize with sort/dist keys
- Load and validate data

### Phase 6: Analytics & Visualization
- Build Tableau dashboards
- Create spending analytics
- Implement budget tracking
- Develop predictive insights

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

---

## 🎓 Skills Demonstrated

- [x] Python Programming
- [x] Data Generation & Simulation
- [x] Git Version Control
- [x] AWS Cloud Services (S3, IAM, Glue)
- [x] ETL Pipeline Development
- [x] PySpark & Distributed Processing
- [x] Data Lake Architecture
- [ ] Data Quality Engineering
- [ ] SQL & Data Modeling
- [ ] Data Visualization
- [ ] Data Warehousing

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

---

## 🔧 How to Run

### Prerequisites
- Python 3.12+
- AWS Account with Glue access
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

---

## 📝 Documentation

Detailed documentation for each phase:
- ✅ Data generation process
- ✅ AWS infrastructure setup
- ✅ ETL pipeline architecture
- Coming: Data quality framework
- Coming: Data warehouse design

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
- **Week 4:** Data quality framework
- **Week 5-6:** Data warehouse implementation
- **Week 7-8:** Dashboard development
- **Week 9:** Documentation & final polish

---

## ⭐ Acknowledgments

This project is part of my portfolio to demonstrate data engineering capabilities for full-time opportunities. Special focus on fintech industry standards including data security, compliance considerations, and production-ready code.

---

## 📄 License

This project is open source and available under the MIT License.

---

**Status:** 🚧 Active Development | Last Updated: January 2026
