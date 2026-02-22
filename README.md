# Personal Finance Data Pipeline
### End-to-End Data Engineering Project

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📊 Project Overview

Building a production-grade personal finance analytics platform that demonstrates end-to-end data engineering skills. This project showcases data pipeline development, cloud architecture, data quality frameworks, SQL analytics, pipeline orchestration, and analytics visualization.

**Business Problem:** Individuals need a comprehensive view of their financial health, spending patterns, and budget tracking to make informed financial decisions.

**Solution:** A scalable, automated data pipeline that ingests, processes, validates, and analyzes financial transaction data to deliver actionable insights through interactive dashboards.

---

## 🎯 Project Goals

- Build realistic financial transaction datasets
- Design and implement ETL/ELT pipelines
- Establish data quality frameworks
- Deploy cloud-based data infrastructure (AWS)
- Create data warehouse with optimized schemas
- **Execute advanced SQL analytics and business intelligence**
- **Orchestrate pipelines with Apache Airflow**
- **Implement monitoring and alerting systems**
- Develop interactive analytics dashboards
- Implement data security best practices

---

## 🛠️ Tech Stack

**Programming & Data Processing:**
- Python 3.12
- Pandas (data manipulation)
- PySpark (distributed processing)
- SQL (data querying & analytics)

**Cloud Platform:**
- AWS S3 (data lake storage)
- AWS Glue (ETL processing)
- AWS Lambda (automation)

**Database:**
- PostgreSQL 15 (data warehouse)
- pgAdmin 4 (database administration)

**Pipeline Orchestration:** ⭐ NEW
- **Apache Airflow 3.1.7**
- DAG scheduling and monitoring
- Task dependencies and workflows

**Data Quality & Testing:**
- Great Expectations
- Pandas validation
- **Automated quality monitoring**
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
├── WEEK9_SUMMARY.md                  # ⭐ NEW
│
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
├── sql/                              # Week 7-8
│   ├── create_schema.sql             # Database schema creation
│   ├── load_data_to_postgres.py      # Data loading script
│   └── week7-8/
│       ├── query_results/            # 18 CSV exports
│       ├── Week7-8_Completion_Report.md
│       └── Week7-8_Insights_Report.md
│
├── airflow/                          # ⭐ Week 9
│   ├── README.md                     # Airflow documentation
│   ├── dags/
│   │   ├── personal_finance_etl_dag.py        # Main ETL pipeline
│   │   ├── pipeline_health_check.py           # Health monitoring
│   │   ├── data_quality_monitoring.py         # Quality checks
│   │   ├── data_quality_checks.py             # Validation module
│   │   ├── idempotency_test.py                # Testing DAG
│   │   └── hello_world_dag.py                 # Tutorial DAG
│   ├── logs/                         # Airflow execution logs
│   └── airflow.cfg                   # Airflow configuration
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
  + Total Transactions: 1,000
  + Total Amount Spent: $146,719.64
  + Average Transaction: $146.72
  + Date Range: 2023-01-01 - 2024-12-13
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

**Cost:** $0.00 (local PostgreSQL installation)

---

### ✅ Phase 7-8: SQL Analytics & Business Intelligence (Completed - Feb 2026) ⭐ NEW

**What I Built:**
- 18 advanced SQL analytical queries
- Comprehensive business insights extraction
- Time-series analysis and trend detection
- Statistical analysis and outlier detection
- Reusable database views for dashboards

**Key Features:**

**Query Categories:**
1. **Basic Aggregations (Q1-Q3)**
   - Overall spending summary
   - Category-level breakdowns
   - Top merchant analysis

2. **Time-Series Analysis (Q4-Q6)**
   - Monthly spending trends
   - Day of week patterns
   - Quarterly comparisons

3. **Window Functions (Q7-Q9)**
   - Running totals
   - Category rankings by month
   - Top N transactions per category

4. **Advanced Window Functions (Q10-Q11)**
   - Month-over-month change calculations
   - 7-day moving averages

5. **Multi-Dimensional Analysis (Q12-Q13)**
   - Payment method × category cross-analysis
   - Weekend vs weekday spending patterns

6. **Behavioral Analysis (Q14-Q15)**
   - Merchant visit frequency and loyalty
   - High-value transaction detection (top 10%)

7. **Business Metrics (Q16-Q18)**
   - Spending velocity and rhythm
   - Category concentration index (Herfindahl)
   - Dashboard view creation

**Technical Skills Mastered:**
- Window functions (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD)
- CTEs (Common Table Expressions) for complex queries
- Running totals with SUM() OVER
- Moving averages with window frames (ROWS BETWEEN)
- Percentile calculations (PERCENTILE_CONT)
- Statistical functions (STDDEV, variance analysis)
- CREATE VIEW for reusable analytics
- Type casting and function compatibility

**Top 5 Business Insights:**

1. **Budget Concentration Risk**
   - 51.21% of spending goes to rent alone
   - Herfindahl Index: 3,139 = "Highly Concentrated"
   - **Action:** Build 3-month emergency fund

2. **Grocery Shopping Inefficiency**
   - Shopping at 4 different grocery stores
   - **Opportunity:** Consolidate to 1-2 stores → save $50-100/month

3. **Missed Credit Card Rewards**
   - Only 13.3% of spending on credit card
   - **Potential gain:** $144-288/year in cashback

4. **Weekend Spending Pattern**
   - Saturdays have highest avg transaction ($505)
   - **Action:** Implement 24-hour wait rule for purchases >$250

5. **High Transaction Frequency**
   - Transaction every 0.71 days (1.4/day average)
   - **Action:** Implement "no-spend days" 2x/week

**Deliverables:**
- ✅ 18 SQL queries executed successfully
- ✅ 18 CSV exports for Tableau visualization
- ✅ Week7-8_Insights_Report.md (50+ pages of analysis)
- ✅ Week7-8_Completion_Report.md (comprehensive documentation)
- ✅ `v_spending_dashboard` view created
- ✅ 50+ actionable insights documented

**Statistics:**
- Queries Executed: 18/18 (100%)
- Lines of SQL: ~600
- Insights Generated: 50+
- Time Invested: ~8 hours
- Documentation: 5,700+ words

**Cost:** $0.00 (runs locally)

---

### ✅ Phase 9: Apache Airflow Pipeline Orchestration (Completed - Feb 2026) ⭐ NEW

**What I Built:**
- Production-ready Apache Airflow 3.1.7 installation
- 4 automated DAGs for ETL, monitoring, and quality checks
- 8-task main pipeline with comprehensive orchestration
- Performance optimization achieving 26x speedup
- Idempotent operations ensuring safe re-runs

**Key Features:**

**Main ETL Pipeline (`personal_finance_etl`):**
- **8 Sequential Tasks:**
  1. Download from S3
  2. Comprehensive data quality validation (8 checks)
  3. Transform data with derived columns
  4. Batch load to PostgreSQL (optimized)
  5. Cleanup temporary files
  6. Print execution summary
  7. Benchmark performance
  8. Track pipeline run metadata

- **Performance Metrics:**
  - **Throughput:** 2,646 rows/second (26x faster than baseline!)
  - **Load Time:** 0.38 seconds for 1,000 rows
  - **Total Pipeline Duration:** ~12 seconds
  - **Optimization:** Batch inserts using `execute_values`

- **Data Quality Validation:**
  - Schema validation (column presence and types)
  - Null value detection in critical fields
  - Duplicate transaction detection
  - Amount range validation ($0-$10,000)
  - Date range validation (no future dates)
  - Category whitelist validation
  - Statistical anomaly detection (3 std dev)
  - Quality score: 100%

- **Production Features:**
  - **Idempotent operations** - safe to re-run without duplicates
  - PRIMARY KEY constraints at database level
  - ON CONFLICT DO NOTHING for graceful duplicate handling
  - 3 automatic retries with exponential backoff
  - Comprehensive error handling and rollback
  - Pipeline run tracking in `pipeline_runs` table

**Supporting DAGs:**

1. **`pipeline_health_check`** (Hourly)
   - Database connection monitoring
   - Data freshness validation (alerts if > 48 hours)
   - Disk space monitoring
   - Log directory size tracking
   - 3 parallel health checks

2. **`data_quality_monitoring`** (Daily at 3 AM)
   - Warehouse-level quality validation
   - Historical quality trend tracking (30 days)
   - Quality report generation
   - 100% quality pass rate

3. **`idempotency_test`** (Manual)
   - Validates no duplicate transaction IDs
   - Verifies PRIMARY KEY constraints
   - Checks table integrity
   - Shows pipeline run history

**Technical Implementation:**
- Apache Airflow 3.1.7 (standalone mode)
- Python operators for task execution
- XCom for inter-task communication
- SLA monitoring (task duration alerts)
- Batch processing with psycopg2.extras.execute_values
- Comprehensive logging and observability

**Database Schema Enhancements:**
```sql
-- Idempotent staging table with PRIMARY KEY
CREATE TABLE staging_transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,  -- Prevents duplicates
    date DATE,
    merchant VARCHAR(100),
    category VARCHAR(50),
    amount DECIMAL(10,2),
    payment_method VARCHAR(50),
    transaction_date TIMESTAMP,
    year INT,
    month INT,
    day_of_week INT,
    week_of_year INT,
    processed_timestamp TIMESTAMP
);

-- Pipeline audit trail
CREATE TABLE pipeline_runs (
    run_id VARCHAR(100) PRIMARY KEY,
    run_date TIMESTAMP,
    run_type VARCHAR(20),              -- 'scheduled' or 'manual'
    rows_processed INT,
    rows_loaded INT,
    total_rows_in_table INT,
    load_duration DECIMAL(10,2),
    throughput DECIMAL(10,2),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Monitoring & Observability:**
- Real-time task status tracking
- Performance benchmarking with historical trends
- Quality metrics over time
- System health dashboards
- Failure alerts and callbacks
- Success tracking and logging

**Schedule:**
- **Main ETL:** Daily at 2:00 AM (automated)
- **Health Check:** Every hour (automated)
- **Quality Monitor:** Daily at 3:00 AM (automated)
- **Testing:** Manual trigger

**Cost:** $0.00 (runs locally)

**Key Achievements:**
- ✅ 26x performance improvement (100 → 2,646 rows/sec)
- ✅ 100% idempotent operations (zero duplicates)
- ✅ 100% data quality score
- ✅ Automated daily execution
- ✅ Comprehensive monitoring (3 monitoring DAGs)
- ✅ Production-ready with retry logic
- ✅ Complete audit trail

---

## 📈 Next Steps

### Phase 10: Tableau Dashboards (Coming Soon)
- Build interactive visualizations using Week 7-8 CSV exports
- Create spending analytics dashboard
- Implement budget tracking views
- Design executive summary dashboard
- Publish to Tableau Public

### Phase 11-12: Web Application
- Build React frontend
- Create interactive UI
- Integrate Tableau dashboards
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

### Week 7-8 Learnings: ⭐ NEW
- **Advanced SQL:** Window functions, CTEs, statistical analysis
- **Window Functions:** ROW_NUMBER, RANK, LAG, LEAD, running totals
- **CTEs:** Breaking complex queries into readable modules
- **Time-Series Analysis:** Monthly trends, moving averages, YoY comparisons
- **Business Intelligence:** Translating data into actionable insights
- **Statistical Analysis:** Percentiles, standard deviation, outlier detection
- **Multi-Dimensional Analysis:** Cross-tabulations, payment × category patterns
- **Behavioral Analytics:** Spending patterns, merchant loyalty, transaction frequency
- **Concentration Metrics:** Herfindahl index for budget distribution risk

### Week 9 Learnings: ⭐ NEW
- **Apache Airflow:** DAG development, task orchestration, scheduling
- **Workflow Automation:** Cron expressions, dependency management, task monitoring
- **Performance Optimization:** Batch operations, connection pooling, throughput maximization
- **Idempotency:** Safe re-runs, duplicate prevention, PRIMARY KEY constraints
- **Observability:** Logging, metrics, XCom, performance tracking
- **Error Handling:** Retry strategies, exponential backoff, rollback mechanisms
- **Production Best Practices:** SLA monitoring, health checks, audit trails
- **Data Quality at Scale:** Automated validation, anomaly detection, trend analysis

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
- [x] **Advanced SQL Analytics** ⭐ NEW
- [x] **Window Functions & CTEs** ⭐ NEW
- [x] **Business Intelligence** ⭐ NEW
- [x] **Statistical Analysis** ⭐ NEW
- [x] **Apache Airflow & DAG Development** ⭐ NEW
- [x] **Pipeline Orchestration & Scheduling** ⭐ NEW
- [x] **Performance Optimization** ⭐ NEW
- [x] **Production Monitoring & Alerting** ⭐ NEW
- [ ] Data Visualization (Tableau)
- [ ] Web Development (React)

---

## 📊 Sample Data Flow

**Bronze Layer (S3 - CSV):**
```csv
transaction_id,date,time,merchant,category,amount,payment_method,status
TXN000239,2023-01-01,05:11,Walmart,Groceries,57.57,Debit Card,Posted
TXN000957,2023-01-02,21:10,Public Transit,Transportation,28.98,Debit Card,Posted
```

**Silver Layer (S3 - Parquet, enriched):**
```
transaction_id, date, merchant, category, amount, year, month, month_name, day_of_week, is_weekend
```

**Gold Layer (PostgreSQL - Star Schema):**
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

**SQL Analytics (Week 7-8):**
```sql
-- Example: Running total with window function
SELECT 
    transaction_date,
    category_name,
    amount,
    SUM(amount) OVER (ORDER BY transaction_date) as running_total
FROM fact_transactions f
JOIN dim_category c ON f.category_key = c.category_key
ORDER BY transaction_date;
```

**Airflow Orchestration (Week 9 - Automated Daily at 2 AM):**
```
Download from S3 → Validate (8 checks) → Transform → 
Load to PostgreSQL (2,646 rows/sec) → Cleanup → 
Track Metrics → Monitor Quality
```

---

## 🔧 How to Run

### Prerequisites
- Python 3.12+
- AWS Account with Glue access
- AWS CLI configured
- PostgreSQL 15+
- Apache Airflow 3.1.7
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

6. **Execute SQL analytics:** ⭐ NEW
```bash
# Open pgAdmin or psql
# Run queries from Week7-8_Insights_Report.md
# Export results to CSV for Tableau
```

7. **Start Apache Airflow:** ⭐ NEW
```bash
# Set environment variables
export no_proxy='*'
export AIRFLOW_HOME=~/Desktop/personal-finance-pipeline/personal-finance-pipeline/airflow

# Navigate to project
cd ~/Desktop/personal-finance-pipeline/personal-finance-pipeline

# Start Airflow
airflow standalone

# Access UI at http://localhost:8080
# Username: admin
# Password: (from simple_auth_manager_passwords.json.generated)
```

---

## 📝 Documentation

Detailed documentation for each phase:
- ✅ Data generation process
- ✅ AWS infrastructure setup
- ✅ ETL pipeline architecture
- ✅ Data quality framework
- ✅ Data warehouse design and implementation
- ✅ **SQL analytics and insights** ⭐ NEW
- ✅ **Apache Airflow orchestration** ⭐ NEW
- ✅ **Pipeline monitoring and alerting** ⭐ NEW
- Coming: Tableau dashboard development

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
- **Week 7-8 (Feb 2026):** ✅ **SQL analytics & business intelligence complete** ⭐
- **Week 9 (Feb 2026):** ✅ **Apache Airflow pipeline orchestration complete** ⭐
- **Week 10:** Tableau dashboards (Coming Soon)
- **Week 11-12:** React web application

---

## 📊 Project Metrics

**Overall Progress:** 75% Complete (9/12 weeks)

**Code & Documentation:**
- **Lines of Code:** 3,500+
- **Lines of SQL:** 600+
- **DAGs Created:** 4 production + 1 tutorial
- **SQL Queries:** 18 analytical queries
- **Documentation:** 8,000+ words

**Data Engineering:**
- **Data Quality Checks:** 8 comprehensive validations
- **Performance Improvement:** 26x faster loading
- **Pipeline Tasks:** 8 orchestrated tasks
- **Data Processed:** 1,000+ transactions
- **CSV Exports:** 18 for Tableau

**Automation & Monitoring:**
- **Scheduled DAGs:** 3 automated (ETL, health, quality)
- **Success Rate:** 100%
- **Quality Pass Rate:** 100%
- **Idempotent Operations:** Yes (safe re-runs)

---

## ⭐ Acknowledgments

This project is part of my portfolio to demonstrate data engineering capabilities for full-time opportunities. Special focus on fintech industry standards including data security, compliance considerations, production-ready code, advanced SQL analytics, and enterprise-grade pipeline orchestration.

---

## 📄 License

This project is open source and available under the MIT License.

---

**Status:** 🚧 Active Development | Last Updated: February 2026 | 75% Complete (9/12 weeks)