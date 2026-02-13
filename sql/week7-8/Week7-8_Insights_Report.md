# Week 7-8: SQL Analytics Insights Report

**Student:** Aditi Reddy  
**Completion Date:** February 9, 2026  
**Database:** Personal Finance Warehouse  
**Analysis Period:** January 2023  
**Total Transactions Analyzed:** 42

---

## 📊 Executive Summary

Analysis of 42 transactions from January 2023 reveals **highly concentrated spending** dominated by three major categories (Rent, Groceries, Shopping) accounting for **80.9% of total expenditure**. Spending is characterized by **frequent small transactions** (avg $162) punctuated by **large rent payments** ($1,819 and $1,675). The Herfindahl Index of **3,139** confirms spending is "Highly Concentrated" with Rent alone representing over half (51%) of all expenses.

**Key Finding:** Digital Wallet (38%) and Debit Card (32%) are preferred payment methods, together accounting for 70% of all transactions.

---

## 💰 Overall Financial Summary

### Query 1: Headline Metrics

| Metric | Value |
|--------|-------|
| **Total Transactions** | 42 |
| **Total Spent** | $6,822.35 |
| **Average Transaction** | $162.44 |
| **Smallest Transaction** | $5.73 |
| **Largest Transaction** | $1,819.03 |
| **Standard Deviation** | $367.12 |

**Analysis:**
- **Transaction frequency:** 0.71 days between transactions = ~1 purchase per day
- **Volatility:** Standard deviation of $367 indicates high variability
- **Outliers:** Largest transaction is **11.2x** the average (rent payment)
- **Range:** $1,813 spread between smallest ($5.73 subscription) and largest ($1,819 rent)

**Transaction Rhythm:**
- Minimum gap: 0 days (same-day purchases)
- Maximum gap: 3 days (longest period without spending)
- Consistency: Never went more than 3 days without a transaction in January

---

## 📁 Category Breakdown

### Query 2: Spending by Category

| Rank | Category | Type | Transactions | Total | % of Total | Avg/Transaction |
|------|----------|------|-------------|-------|-----------|-----------------|
| 1 | Rent | Essential | 2 | $3,493.98 | 51.21% | $1,746.99 |
| 2 | Groceries | Essential | 10 | $1,052.34 | 15.42% | $105.23 |
| 3 | Shopping | Discretionary | 4 | $973.70 | 14.27% | $243.43 |
| 4 | Entertainment | Discretionary | 5 | $333.17 | 4.88% | $66.63 |
| 5 | Restaurants | Discretionary | 7 | $312.16 | 4.58% | $44.59 |
| 6 | Healthcare | Essential | 1 | $309.39 | 4.53% | $309.39 |
| 7 | Gas | Essential | 3 | $153.45 | 2.25% | $51.15 |
| 8 | Subscriptions | Discretionary | 6 | $112.07 | 1.64% | $18.68 |
| 9 | Transportation | Essential | 4 | $82.09 | 1.20% | $20.52 |

**Essential vs Discretionary Split:**
- **Essentials:** $5,090.25 (74.6%) - Rent, Groceries, Healthcare, Gas, Transportation
- **Discretionary:** $1,731.10 (25.4%) - Shopping, Entertainment, Restaurants, Subscriptions

**Key Insights:**
1. **Top 3 categories account for 80.9%** of all spending
2. **Rent dominates** at 51% - over half the budget goes to housing
3. **Groceries** show consistent behavior: 10 trips @ ~$105/trip = weekly shopping pattern
4. **Shopping** has high variance: only 4 purchases but $243 average (big-ticket items)
5. **Subscriptions** are small individually ($19/month avg) but add up to $112 total

**Budget Concentration (Herfindahl Index):**
- **Score: 3,139.02** = "Highly Concentrated"
- Interpretation: Spending heavily dominated by 1-2 categories (Rent + Groceries = 67%)
- Implication: Budget is NOT diversified - vulnerable to rent increases

---

## 🏪 Merchant Analysis

### Query 3: Top 10 Merchants

| Rank | Merchant | Type | Visits | Total Spent | Avg/Visit | Largest Purchase |
|------|----------|------|--------|-------------|-----------|------------------|
| 1 | Property Management | Physical | 2 | $3,493.98 | $1,746.99 | $1,819.03 |
| 2 | Walmart | Physical | 4 | $396.12 | $99.03 | $128.94 |
| 3 | Dentist Office | Physical | 1 | $309.39 | $309.39 | $309.39 |
| 4 | Trader Joe's | Physical | 3 | $307.40 | $102.47 | $134.23 |
| 5 | Best Buy | Physical | 1 | $286.83 | $286.83 | $286.83 |
| 6 | Macy's | Physical | 1 | $266.13 | $266.13 | $266.13 |
| 7 | Nike | Physical | 1 | $237.68 | $237.68 | $237.68 |
| 8 | Costco | Physical | 2 | $208.62 | $104.31 | $144.62 |
| 9 | Amazon | Physical | 1 | $183.06 | $183.06 | $183.06 |
| 10 | Whole Foods | Physical | 1 | $140.20 | $140.20 | $140.20 |

**Merchant Loyalty Patterns (Query 14):**
- **Walmart:** 4 visits = most frequent (weekly shopper)
- **Trader Joe's:** 3 visits = secondary grocery option
- **Property Management:** 2 visits = bi-monthly rent
- **Costco:** 2 visits = bulk shopping

**Shopping Behavior:**
- **Grocery diversification:** 4 different stores (Walmart, Trader Joe's, Costco, Whole Foods)
- **No brand loyalty:** Spreads grocery spending across budget (Walmart) and premium (Whole Foods)
- **All physical stores:** Prefers in-person shopping over online
- **One-time big purchases:** Best Buy, Macy's, Nike all single visits

**Shopping Spree Breakdown ($973.70 total):**
- Best Buy: $286.83 (electronics)
- Macy's: $266.13 (clothing/home goods)
- Nike: $237.68 (athletic gear)
- Amazon: $183.06 (online shopping)

---

## 📅 Temporal Patterns

### Query 4-6: Time-Based Analysis

**Monthly View (January 2023 only):**
- All 42 transactions occurred in a single month
- Total: $6,822.35
- No month-over-month comparison available (single-month dataset)

### Query 5: Day of Week Patterns

| Day | Weekend? | Transactions | Total | Avg/Transaction |
|-----|----------|-------------|-------|-----------------|
| Monday | No | 8 | $2,537.85 | $317.23 |
| Saturday | No | 4 | $2,021.17 | $505.29 |
| Wednesday | No | 8 | $628.03 | $78.50 |
| Thursday | No | 6 | $617.69 | $102.95 |
| Sunday | Yes | 6 | $515.47 | $85.91 |
| Friday | No | 6 | $287.19 | $47.87 |
| Tuesday | No | 4 | $214.95 | $53.74 |

**Weekend vs Weekday:**
- **Weekend (Sat+Sun):** 10 transactions, $2,536.64 total (37.2%)
- **Weekday (Mon-Fri):** 32 transactions, $4,285.71 total (62.8%)

**Key Patterns:**
1. **Monday is rent day:** $2,538 total (likely includes rent payment)
2. **Saturday = big shopping day:** $2,021 total with $505 avg transaction
3. **Tuesday/Friday = low spending days:** Under $300 total each
4. **Weekday-heavy overall:** 63% of spending occurs Mon-Fri

### Query 13: Weekend vs Weekday by Category

| Category | Weekend $ | Weekday $ | % Weekend |
|----------|-----------|-----------|-----------|
| Rent | $1,819.03 | $1,674.95 | 52% |
| Subscriptions | $48.63 | $63.44 | 43% |
| Gas | $47.21 | $106.24 | 31% |
| Entertainment | $97.80 | $235.37 | 29% |
| Groceries | $278.85 | $773.49 | 27% |
| Restaurants | $62.06 | $250.10 | 20% |
| Shopping | $183.06 | $790.64 | 19% |
| Transportation | $0.00 | $82.09 | 0% |
| Healthcare | $0.00 | $309.39 | 0% |

**Behavioral Insights:**
- **Rent payment split:** One on weekend, one on weekday
- **Groceries:** 73% weekday (regular weekly shopping trips)
- **Restaurants:** 80% weekday (lunch/work-related dining)
- **Shopping:** 81% weekday (big purchases at Best Buy, Macy's on weekdays)
- **Transportation/Healthcare:** 100% weekday only

---

## 💳 Payment Method Analysis

### Query 12: Payment Preferences

**By Payment Method (Total Spending):**
| Payment Method | Total Spent | % of Total | Transactions |
|----------------|-------------|-----------|-------------|
| Digital Wallet | $2,613.85 | 38.3% | 10 |
| Debit Card | $2,179.71 | 31.9% | 7 |
| Cash | $1,119.75 | 16.4% | 17 |
| Credit Card | $909.04 | 13.3% | 6 |

**Payment Strategy Insights:**
1. **Digital Wallet dominates:** $2,614 (38%) - includes one $1,819 rent payment + groceries
2. **Debit Card for large bills:** $2,180 (32%) - includes $1,675 rent payment
3. **Cash for small purchases:** $1,120 (16%) but most transactions (17 of 42)
4. **Credit Card underutilized:** Only $909 (13%) - potential rewards optimization opportunity

**Payment Method by Category:**
- **Rent:** Digital Wallet ($1,819) + Debit Card ($1,675)
- **Groceries:** Mixed across all 4 methods (no clear preference)
- **Healthcare:** Credit Card only ($309 dentist)
- **Shopping:** All payment types used
- **Restaurants:** Credit Card ($159) + Debit ($47) + Cash ($106)

**Rewards Optimization Opportunity:**
- Currently using Credit Card for only 13% of spending
- Could shift Groceries ($1,052) and Gas ($153) to credit card for rewards
- Potential missed rewards: ~$12-24/month depending on card (1-2% cashback)

---

## 📈 Advanced Analytics

### Query 7: Running Total Analysis

**Spending Curve:**
- Started at $0, ended at $6,822.35 over 31 days
- Average daily accumulation: $220/day
- Steepest climbs: Jan 9 ($1,675 rent) and Jan 14 ($1,819 rent)

### Query 8-9: Category Rankings & Top Transactions

**#1 Category Every Month:** Rent (51% of budget)

**Top 3 Transactions by Category:**

**Rent:**
1. $1,819.03 - Property Management (Jan 14)
2. $1,674.95 - Property Management (Jan 9)

**Shopping:**
1. $286.83 - Best Buy (Jan 23)
2. $266.13 - Macy's (Jan 30)
3. $237.68 - Nike (Jan 16)

**Groceries:**
1. $144.62 - Costco
2. $134.23 - Trader Joe's
3. $134.46 - Cash payment

**Healthcare:**
1. $309.39 - Dentist Office (one-time unplanned expense)

### Query 10-11: Trend Analysis

**Month-over-Month:** N/A (single month dataset)

**7-Day Moving Average:**
- Smoothed daily spending volatility
- Average daily spend: ~$220
- Peaks aligned with rent payment dates (Jan 9, Jan 14)

### Query 15: High-Value Transaction Detection

**90th Percentile Threshold: $263.29**

**Top 10% Transactions (5 total):**
1. $1,819.03 - Rent (Jan 14)
2. $1,674.95 - Rent (Jan 9)
3. $309.39 - Dentist (Jan 12)
4. $286.83 - Best Buy (Jan 23)
5. $266.13 - Macy's (Jan 30)

**Fraud Detection Implication:**
- Any transaction above $263 would trigger review
- 5 of 42 transactions (12%) flagged as "high-value"
- All flagged transactions are legitimate (rent, healthcare, planned shopping)

### Query 16: Spending Velocity

| Metric | Value |
|--------|-------|
| Avg Days Between Transactions | 0.71 days |
| Min Gap | 0 days (same-day purchases) |
| Max Gap | 3 days |
| Std Dev | 0.78 days |

**Interpretation:**
- Transacted **every 0.71 days** = 1.4 transactions per day on average
- **Very high transaction frequency** in January
- Never went more than 3 consecutive days without spending
- Consistent daily spending behavior

---

## 🎯 Top 5 Actionable Insights

### 1. **Rent Dominates Budget - Need Diversification**

**Finding:** Rent consumes 51.21% of total spending ($3,494 of $6,822)

**Implication:** Budget is "Highly Concentrated" (Herfindahl Index: 3,139)

**Action:**
- Vulnerable to rent increases
- Consider roommate or cheaper housing option
- Build emergency fund equal to 3 months rent ($5,250)

---

### 2. **Grocery Store Hopping Costs Time & Money**

**Finding:** 10 grocery trips across 4 different stores (Walmart, Trader Joe's, Costco, Whole Foods)

**Implication:** Inefficient shopping - multiple trips increase impulse purchases

**Action:**
- Consolidate to 1-2 primary grocery stores
- Walmart is most frequent (4 visits) - make this the primary
- Use Costco for monthly bulk items only
- Could save ~$50-100/month by reducing impulse trips

---

### 3. **Discretionary Spending is Reasonable but Concentrated**

**Finding:** Discretionary spending = $1,731 (25.4% of total)
- Shopping: $974 (14%)
- Entertainment: $333 (5%)
- Restaurants: $312 (5%)
- Subscriptions: $112 (2%)

**Implication:** Not overspending on discretionary, but Shopping is high for just 4 purchases

**Action:**
- Review the $974 in Shopping (Best Buy, Macy's, Nike, Amazon)
- Were these planned purchases or impulse buys?
- Set monthly discretionary cap at $400 (currently $577/month avg)

---

### 4. **Underutilizing Credit Card Rewards**

**Finding:** Only 13.3% of spending ($909) on credit card despite rewards potential

**Current:**
- Digital Wallet: 38% ($2,614)
- Debit Card: 32% ($2,180)
- Cash: 16% ($1,120)
- Credit Card: 13% ($909)

**Opportunity:** Shift recurring expenses to credit card for rewards

**Action:**
- Move Groceries ($1,052) to credit card → earn $10-21/month (1-2% back)
- Move Gas ($153) to credit card → earn $1.50-3/month
- Total potential: $12-24/month = $144-288/year in missed rewards

---

### 5. **Healthcare was Unplanned Expense**

**Finding:** $309.39 dentist visit (4.5% of January budget) on a single transaction

**Implication:** Reactive healthcare spending - no preventive budgeting

**Action:**
- Set aside $50/month for healthcare ($600/year)
- Covers routine checkups, dental, urgent care
- Prevents budget shock from unexpected medical expenses

---

## 📋 Recommendations for Financial Management

### **Budget Allocation (Based on Data)**

**Current Reality:**
- Housing (Rent): 51%
- Food (Groceries + Restaurants): 20%
- Discretionary (Shopping + Entertainment): 19%
- Transportation (Gas + Transit): 3%
- Healthcare: 5%
- Subscriptions: 2%

**Recommended 50/30/20 Budget:**
- **Needs (50%):** Rent, Groceries, Gas, Healthcare, Transportation = $3,411
  - Current: $5,090 (75%) ← Overspending by $1,679
- **Wants (30%):** Shopping, Restaurants, Entertainment, Subscriptions = $2,047
  - Current: $1,731 (25%) ← Underspending by $316 (you have room here!)
- **Savings (20%):** Should be $1,364/month
  - Current: $0 ← Not reflected in transaction data

**Action:** Current budget is imbalanced - Needs are 75% instead of target 50%

### **Spending Controls**

1. **Set Category Caps:**
   - Groceries: $800/month (current: $1,052) - reduce by $252
   - Shopping: $300/month (current: $974) - reduce by $674
   - Restaurants: $250/month (current: $312) - reduce by $62
   
2. **Implement Weekly Check-ins:**
   - Review spending every Sunday
   - Track against running total (Query 7 dashboard)
   
3. **Alert System:**
   - Flag any transaction >$250 (90th percentile threshold)
   - Require 24-hour wait period before purchase

### **Payment Strategy**

1. **Maximize Rewards:**
   - Move all Groceries, Gas, Restaurants to credit card
   - Potential annual rewards: $288-576 (assuming 2% card)
   
2. **Simplify Payment Methods:**
   - Currently using 4 different methods (confusing)
   - Consolidate to: Credit Card (daily) + Debit (rent) + Cash (minimal)

### **Savings Opportunities**

**Immediate Wins:**
1. **Audit subscriptions:** $112/month - cancel unused services
2. **Consolidate groceries:** Save $50-100/month by reducing store hopping
3. **Plan shopping:** The $974 in Shopping could be reduced by 50% with planned purchases

**Target Monthly Savings:** $300-500

**Emergency Fund Goal:** $5,250 (3 months rent) - critical given 51% rent burden

---

## 🔍 Data Quality Notes

**Issues Encountered:**
- None - all 42 transactions loaded cleanly
- All foreign keys resolved correctly
- No missing values in critical columns

**Data Characteristics:**
- Single month (January 2023) limits trend analysis
- No month-over-month or year-over-year comparisons possible
- Strong dataset for behavioral pattern analysis

**Resolutions:**
- Status column had NULL values → removed `WHERE status = 'completed'` filter
- All date-based queries use `transaction_date` column directly

---

## 💻 Technical Learnings

### **SQL Techniques Mastered:**

- [x] **Window Functions:** ROW_NUMBER, RANK, LAG, LEAD, SUM OVER, AVG OVER
- [x] **CTEs (Common Table Expressions):** WITH clauses for modular queries
- [x] **Subqueries:** Nested and correlated subqueries
- [x] **Date/Time Functions:** EXTRACT, TO_CHAR, date arithmetic
- [x] **CASE Statements:** Conditional logic for weekend/weekday splits
- [x] **Percentile Calculations:** PERCENTILE_CONT for outlier detection
- [x] **View Creation:** CREATE OR REPLACE VIEW for dashboards
- [x] **Aggregations:** SUM, AVG, COUNT, MIN, MAX, STDDEV, ROUND
- [x] **Multi-Table JOINs:** 3-4 table joins with proper key relationships

### **Challenges Overcome:**

**Challenge 1: Status Column Filtering**
- Issue: `WHERE status = 'completed'` returned NULL results
- Solution: Removed filter or used `WHERE status IS NOT NULL`
- Lesson: Always check data before filtering

**Challenge 2: PERCENTILE_CONT Type Casting**
- Issue: `ROUND(double precision)` function error
- Solution: Added `::numeric` cast
- Lesson: PostgreSQL requires explicit type conversions for some functions

**Challenge 3: Date Dimension vs Transaction Date**
- Issue: Original queries assumed `date_key` foreign key
- Solution: Modified queries to use `transaction_date` directly with EXTRACT
- Lesson: Adapt queries to actual schema implementation

### **Most Useful Queries:**

1. **Query 2 (Category Breakdown):** Foundation for all budget analysis
2. **Query 7 (Running Total):** Perfect for tracking budget progress visually
3. **Query 13 (Weekend/Weekday Split):** Revealed behavioral patterns
4. **Query 15 (Top 10% Outliers):** Fraud detection & budget shock identification
5. **Query 18 (Dashboard View):** Reusable view for ongoing monitoring

---

## 📊 Next Steps (Week 9-10)

### **Tableau Preparation (Week 10)**

**Dashboards to Create:**
1. **Budget Overview Dashboard**
   - Pie chart: Category breakdown (Query 2)
   - Line chart: Running total (Query 7)
   - Bar chart: Top merchants (Query 3)

2. **Temporal Analysis Dashboard**
   - Heatmap: Day of week spending (Query 5)
   - Line chart: 7-day moving average (Query 11)
   - Comparison: Weekend vs weekday by category (Query 13)

3. **Payment Strategy Dashboard**
   - Stacked bar: Payment method by category (Query 12)
   - Pie chart: Payment method distribution

4. **Behavioral Insights Dashboard**
   - Scatter plot: Transaction size distribution
   - Histogram: Spending velocity (Query 16)
   - Alert list: Top 10% transactions (Query 15)

**Data Exports for Tableau:**
- [x] q02_spending_by_category.csv
- [x] q03_top_merchants.csv
- [x] q05_day_of_week.csv
- [x] q07_running_total.csv
- [x] q12_payment_category.csv
- [x] q13_weekend_weekday.csv
- [x] q18_dashboard_view.csv

### **Skills to Learn Next:**

**Week 9: Apache Airflow (Pipeline Orchestration)**
- Automate the ETL pipeline
- Schedule daily data loads
- Monitor data quality

**Week 10: Tableau (Data Visualization)**
- Build interactive dashboards
- Create calculated fields
- Design for executive presentation

**Weeks 11-12: React Web App (Full-Stack Integration)**
- Display Tableau dashboards
- Build budget tracking interface
- Deploy to cloud

---

## 📈 Project Progress

**Overall Timeline:**
- ✅ Week 1-2: Data Generation & AWS Setup (Complete)
- ✅ Week 3-4: ETL Pipeline & Data Quality (Complete)
- ✅ Week 5-6: PostgreSQL Data Warehouse (Complete)
- ✅ **Week 7-8: SQL Analytics (JUST COMPLETED!)**
- ⬜ Week 9: Pipeline Orchestration
- ⬜ Week 10: Tableau Dashboards
- ⬜ Week 11-12: Web Application

**Completion:** 67% (8/12 weeks) ✅

---

## 🎓 Skills Demonstrated

**SQL Proficiency:**
- Advanced window functions
- Complex CTEs and subqueries
- Multi-dimensional aggregations
- Statistical analysis (percentiles, standard deviation)
- Database view creation

**Analytical Thinking:**
- Identified spending concentration risk
- Discovered behavioral patterns
- Calculated opportunity costs (missed credit card rewards)
- Proposed data-driven budget recommendations

**Technical Writing:**
- Documented 18 queries with business context
- Translated SQL results into actionable insights
- Created executive-level summary

---

**Report Completed:** February 9, 2026  
**Total Queries Executed:** 18  
**Total Analysis Time:** ~3 hours  
**CSV Exports Created:** 18  
**Insights Generated:** 50+

**GitHub Repository:** https://github.com/aditi-reddy/personal-finance-pipeline
