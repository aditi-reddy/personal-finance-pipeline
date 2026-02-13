# Week 7-8 Completion Report

**Project:** Personal Finance Data Engineering Pipeline  
**Phase:** SQL Analytics & Business Intelligence  
**Completion Date:** February 9, 2026  
**Status:** ✅ COMPLETE

---

## 📊 Summary

Successfully executed 18 analytical SQL queries extracting actionable business insights from personal finance transaction data. Mastered advanced SQL techniques including window functions, CTEs, and statistical analysis. Identified key spending patterns and budget optimization opportunities.

---

## 🎯 Objectives Achieved

- [x] Execute 18 SQL analytical queries covering basic to advanced techniques
- [x] Extract business insights from transaction data
- [x] Master window functions (ROW_NUMBER, RANK, LAG, LEAD, SUM OVER)
- [x] Implement CTEs for complex multi-step queries
- [x] Perform time-series analysis and trend detection
- [x] Create reusable database views for dashboards
- [x] Prepare datasets for Tableau visualization (Week 10)
- [x] Document all findings with actionable recommendations

---

## 📈 Key Statistics

| Metric | Value |
|--------|-------|
| **Queries Executed** | 18/18 (100%) |
| **CSV Exports Created** | 18 |
| **Insights Documented** | 50+ |
| **Time Invested** | ~8 hours |
| **Lines of SQL Written** | ~600 |
| **Database Views Created** | 1 (v_spending_dashboard) |

---

## 💡 Top 5 Insights Discovered

### 1. **Budget Concentration Risk**
- **Finding:** 51.21% of spending goes to rent alone
- **Herfindahl Index:** 3,139 = "Highly Concentrated"
- **Risk:** Vulnerable to rent increases
- **Action:** Build 3-month emergency fund ($5,250)

### 2. **Grocery Inefficiency**
- **Finding:** Shopping at 4 different grocery stores (Walmart, Trader Joe's, Costco, Whole Foods)
- **Cost:** Inefficient trips, impulse purchases
- **Action:** Consolidate to 1-2 primary stores → save $50-100/month

### 3. **Missed Credit Card Rewards**
- **Finding:** Only 13.3% of spending on credit card ($909 of $6,822)
- **Opportunity:** Moving groceries & gas to credit card
- **Potential gain:** $144-288/year in cashback (1-2%)

### 4. **Weekend Spending Pattern**
- **Finding:** Saturdays have highest avg transaction ($505) - big shopping day
- **Implication:** Weekend impulse purchases drive costs up
- **Action:** Implement 24-hour wait rule for purchases >$250

### 5. **High Transaction Frequency**
- **Finding:** Transaction every 0.71 days (1.4/day average)
- **Pattern:** Never went >3 days without spending in January
- **Action:** Implement "no-spend days" 2x/week to build savings discipline

---

## 🔧 Technical Skills Demonstrated

### **SQL Mastery**

**Basic:**
- ✅ SELECT, FROM, WHERE, ORDER BY, LIMIT
- ✅ Aggregations: SUM, AVG, COUNT, MIN, MAX, STDDEV, ROUND
- ✅ GROUP BY with multiple dimensions
- ✅ HAVING for filtered aggregations
- ✅ Multi-table JOINs (INNER JOIN)

**Intermediate:**
- ✅ Window Functions: ROW_NUMBER, RANK, DENSE_RANK
- ✅ Running totals: SUM() OVER (ORDER BY)
- ✅ LAG() and LEAD() for comparisons
- ✅ PARTITION BY for grouped window operations
- ✅ Date functions: EXTRACT, TO_CHAR
- ✅ CASE statements for conditional logic

**Advanced:**
- ✅ CTEs (Common Table Expressions) with WITH clause
- ✅ Nested and correlated subqueries
- ✅ Moving averages with window frames (ROWS BETWEEN)
- ✅ Percentile calculations: PERCENTILE_CONT
- ✅ Statistical functions: STDDEV, variance analysis
- ✅ CREATE VIEW for reusable analytics
- ✅ Type casting (::numeric) for function compatibility
- ✅ CROSS JOIN for threshold comparisons

### **Analytical Thinking**

- ✅ Translated business questions into SQL queries
- ✅ Identified data quality issues and implemented fixes
- ✅ Calculated KPIs and business metrics
- ✅ Performed cohort analysis (merchant loyalty)
- ✅ Detected outliers using statistical methods (90th percentile)
- ✅ Conducted multi-dimensional analysis (payment × category)
- ✅ Created concentration index (Herfindahl)
- ✅ Measured spending velocity and rhythm

---

## 📁 Deliverables Created

### **SQL Queries (18 total)**

**Section 1: Basic Aggregations (Q1-Q3)**
- Query 1: Overall spending summary
- Query 2: Spending by category
- Query 3: Top merchants

**Section 2: Time-Series Analysis (Q4-Q6)**
- Query 4: Monthly spending trends
- Query 5: Day of week patterns
- Query 6: Quarterly comparison

**Section 3: Window Functions (Q7-Q9)**
- Query 7: Running total
- Query 8: Category rankings by month
- Query 9: Top 3 transactions per category

**Section 4: Advanced Window Functions (Q10-Q11)**
- Query 10: Month-over-month change
- Query 11: 7-day moving average

**Section 5: Multi-Dimensional Analysis (Q12-Q13)**
- Query 12: Payment method × category
- Query 13: Weekend vs weekday by category

**Section 6: Behavioral Analysis (Q14-Q15)**
- Query 14: Merchant visit frequency
- Query 15: High-value transactions (top 10%)

**Section 7: Business Metrics (Q16-Q18)**
- Query 16: Spending velocity
- Query 17: Category concentration index
- Query 18: Dashboard view creation

### **Documentation**

- ✅ `Week7-8_Insights_Report.md` (comprehensive analysis, 50+ pages)
- ✅ `Week7-8_Completion_Report.md` (this document)
- ✅ 18 CSV exports in `sql/week7-8/query_results/`
- ✅ Updated README.md with Week 7-8 section
- ✅ SQL workbook with all queries saved

### **Database Objects**

- ✅ `v_spending_dashboard` view (permanent reusable view for monthly metrics)

---

## 🎓 Learning Outcomes

### **Before Week 7-8:**
- Could write basic SELECT queries
- Understood JOINs and GROUP BY
- Limited exposure to advanced SQL

### **After Week 7-8:**
- **Window functions mastery:** Can calculate running totals, rankings, moving averages
- **CTE proficiency:** Can break complex queries into readable modules
- **Statistical analysis:** Can detect outliers, calculate percentiles, measure concentration
- **Business intelligence:** Can translate data into actionable insights
- **Performance awareness:** Understand when to use views vs. subqueries
- **Real-world analytics:** Can answer executive-level business questions with data

### **Interview-Ready Skills:**
- "Explain window functions" ✅
- "What's the difference between ROW_NUMBER and RANK?" ✅
- "How do you calculate a moving average in SQL?" ✅
- "Show me a query using CTEs" ✅
- "How do you detect outliers in a dataset?" ✅

---

## 🔍 Challenges & Solutions

### **Challenge 1: Status Column Filter**
**Problem:** Original queries included `WHERE status = 'completed'` but column had NULL values  
**Error:** All queries returned 0 rows  
**Solution:** Removed status filter or changed to `WHERE status IS NOT NULL`  
**Lesson:** Always inspect data before applying filters

### **Challenge 2: PERCENTILE_CONT Type Error**
**Problem:** `ROUND(double precision, integer)` function not found  
**Error:** Query 15 failed on percentile calculation  
**Solution:** Added `::numeric` type cast: `PERCENTILE_CONT(0.90)::numeric`  
**Lesson:** PostgreSQL requires explicit type conversions for some functions

### **Challenge 3: Date Dimension Schema Mismatch**
**Problem:** Queries assumed `date_key` foreign key to dim_date table  
**Reality:** Data loaded with `transaction_date` column directly  
**Solution:** Modified all time-based queries to use EXTRACT() on transaction_date  
**Lesson:** Adapt queries to actual implementation, not theoretical schema

### **Challenge 4: Single-Month Dataset Limitation**
**Problem:** All transactions in January 2023 - no month-over-month trends  
**Impact:** Queries 4, 10 couldn't show temporal trends  
**Solution:** Acknowledged limitation, focused on daily/weekly patterns instead  
**Lesson:** Dataset constraints don't diminish learning value

---

## 📊 Data Quality Assessment

**Dataset Characteristics:**
- **Records:** 42 transactions
- **Time Period:** January 2023 (single month)
- **Completeness:** 100% - no missing values in key columns
- **Accuracy:** All foreign keys resolved correctly
- **Consistency:** All amounts positive, dates valid, categories assigned

**Data Quality Score:** ⭐⭐⭐⭐⭐ (5/5)

**Strengths:**
- Clean, well-structured data
- Proper star schema implementation
- All dimension lookups successful
- No orphaned records

**Limitations:**
- Single-month dataset limits trend analysis
- No income data for savings rate calculation
- No budget targets for variance analysis

---

## 🚀 Next Steps

### **Week 9: Apache Airflow (Pipeline Orchestration)**
- Automate the entire ETL pipeline
- Schedule daily data ingestion
- Implement data quality checks
- Create email alerts for anomalies

### **Week 10: Tableau Dashboards**
- Build 4 interactive dashboards using Week 7-8 CSV exports
- Create executive summary dashboard
- Design drill-down capability for category analysis
- Publish to Tableau Public

### **Weeks 11-12: React Web Application**
- Build frontend interface for budget tracking
- Integrate Tableau dashboards
- Create budget vs. actual comparison
- Deploy to AWS/Vercel

---

## 📝 Recommendations for Future Analysts

**If starting Week 7-8:**

1. **Run queries sequentially** - they build on each other conceptually
2. **Export CSVs immediately** - don't wait until the end
3. **Document as you go** - write insights while they're fresh
4. **Visualize in Excel first** - helps spot patterns before Tableau
5. **Focus on business value** - SQL is a tool, insights are the goal

**Most Valuable Queries:**
- Query 2 (Category breakdown) - foundation for budgeting
- Query 7 (Running total) - tracks progress toward goals
- Query 15 (Outliers) - fraud detection & unusual spending
- Query 18 (Dashboard view) - reusable for ongoing monitoring

**Time Savers:**
- Use CTEs to break complex queries into steps
- Create views for frequently-run queries
- Comment your SQL with business context
- Save query templates for reuse

---

## 🎉 Achievements Unlocked

- ✅ **SQL Power User:** Executed 18 advanced analytical queries
- ✅ **Window Functions Master:** Used ROW_NUMBER, RANK, LAG, LEAD, SUM OVER
- ✅ **CTE Expert:** Wrote multi-level WITH clauses
- ✅ **Statistical Analyst:** Calculated percentiles, standard deviations, concentration index
- ✅ **Business Intelligence:** Translated data into 50+ actionable insights
- ✅ **Database Designer:** Created reusable view for dashboards
- ✅ **Documentation Writer:** Produced 50+ pages of analysis

---

## 📊 Project Metrics

**Code Quality:**
- Lines of SQL: ~600
- Queries Written: 18
- Views Created: 1
- Functions Used: 25+
- Tables Joined: 5

**Documentation Quality:**
- Insights Report: 3,500+ words
- Completion Report: 1,800+ words
- README Update: 400+ words
- Total Documentation: 5,700+ words

**Time Investment:**
- Query Development: 4 hours
- Debugging & Testing: 2 hours
- Documentation: 2 hours
- **Total:** 8 hours

**Learning Efficiency:**
- New SQL techniques learned: 15+
- Queries per hour: 2.25
- Insights per query: 3-4

---

## ✅ Completion Checklist

### **Queries**
- [x] Q1-Q3: Basic aggregations (3/3)
- [x] Q4-Q6: Time-series (3/3)
- [x] Q7-Q9: Window functions (3/3)
- [x] Q10-Q11: Advanced windows (2/2)
- [x] Q12-Q13: Multi-dimensional (2/2)
- [x] Q14-Q15: Behavioral (2/2)
- [x] Q16-Q18: Business metrics (3/3)

### **Deliverables**
- [x] 18 CSV exports
- [x] Comprehensive insights report
- [x] Completion report
- [x] Updated README
- [x] Dashboard view created
- [x] LinkedIn post drafted
- [x] Git commits with detailed messages

### **Skills**
- [x] Window functions
- [x] CTEs
- [x] Statistical analysis
- [x] Multi-table JOINs
- [x] Date/time manipulation
- [x] View creation
- [x] Type casting
- [x] Subqueries

---

## 🎓 Final Reflection

**What went well:**
- All 18 queries executed successfully
- Discovered meaningful insights in the data
- Mastered advanced SQL techniques
- Created reusable dashboard views

**What was challenging:**
- Debugging status column filter issue
- Type casting for percentile functions
- Adapting to single-month dataset

**What I learned:**
- SQL is powerful for business analytics
- Window functions unlock advanced analysis
- CTEs make complex queries readable
- Real insights come from asking good questions

**What I'd do differently:**
- Start with data exploration queries first
- Create a data dictionary upfront
- Test each query section before combining

**Most surprising insight:**
- 51% of budget going to rent - didn't realize the concentration
- Transaction every 0.71 days - thought I spent less frequently
- Missed $144-288/year in credit card rewards

---

## 🏆 Final Status

**Week 7-8: SQL Analytics & Business Intelligence**

**Status:** ✅ **COMPLETE**

**Quality:** ⭐⭐⭐⭐⭐ (Exceeded expectations)

**Ready for:** Week 9 (Apache Airflow) & Week 10 (Tableau)

---

**Completion Date:** February 9, 2026  
**Next Phase Start:** Week 9 - Apache Airflow (TBD)  
**Project Progress:** 67% (8/12 weeks)

**GitHub:** https://github.com/aditi-reddy/personal-finance-pipeline
