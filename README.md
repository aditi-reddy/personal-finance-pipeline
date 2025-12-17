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
├── etl/                          # Coming soon
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

## 📈 Next Steps

### Phase 2: AWS Infrastructure Setup (In Progress)
- Set up AWS account and IAM roles
- Create S3 buckets (raw, processed, archive layers)
- Implement folder partitioning strategy
- Configure security policies

### Phase 3: ETL Pipeline Development
- Build AWS Glue jobs for data transformation
- Implement data cleaning and validation
- Create incremental loading logic
- Add error handling and logging

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

---

## 🎓 Skills Demonstrated

- [x] Python Programming
- [x] Data Generation & Simulation
- [x] Git Version Control
- [ ] AWS Cloud Services
- [ ] ETL Pipeline Development
- [ ] Data Quality Engineering
- [ ] SQL & Data Modeling
- [ ] Data Visualization
- [ ] Data Security & Privacy

---

## 📊 Sample Data
```csv
transaction_id,date,time,merchant,category,amount,payment_method,status
TXN000239,2023-01-01,05:11,Walmart,Groceries,57.57,Debit Card,Posted
TXN000957,2023-01-02,21:10,Public Transit,Transportation,28.98,Debit Card,Posted
TXN000247,2023-01-04,08:23,Walmart,Groceries,119.44,Debit Card,Posted
```

---

## 🔧 How to Run

### Prerequisites
- Python 3.12+
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

3. **View the generated data:**
```bash
cd ..
head data/transactions.csv
```

---

## 📝 Documentation

Detailed documentation for each phase will be added as the project progresses:
- Architecture diagrams
- Data dictionary
- ETL process flows
- Setup guides
- Lessons learned

---

## 🤝 Connect With Me

**Aditi Malla**
- 📧 Email: aditireddy205@gmail.com
- 💼 LinkedIn: [linkedin.com/in/aditi-reddy-275a70222](http://www.linkedin.com/in/aditi-reddy-275a70222)
- 🎓 MS Information Systems @ Central Michigan University

---

## 📌 Project Timeline

- **Week 1 (Dec 2024):** ✅ Data generation complete
- **Week 2-3:** AWS infrastructure setup
- **Week 4-5:** ETL pipeline development
- **Week 6-7:** Data quality framework
- **Week 8-9:** Data warehouse implementation
- **Week 10-11:** Dashboard development
- **Week 12:** Documentation & final polish

---

## ⭐ Acknowledgments

This project is part of my portfolio to demonstrate data engineering capabilities for full-time opportunities. Special focus on fintech industry standards including data security, compliance considerations, and production-ready code.

---

## 📄 License

This project is open source and available under the MIT License.

---

**Status:** 🚧 Active Development | Last Updated: December 2025
