# 🍔 Food Delivery ETL & Analytics Pipeline

A practical Data Engineering and Analytics project demonstrating the complete journey of food-delivery order data:

**Data Source → Extraction → Validation → Cleaning → Transformation → PostgreSQL → SQL Analytics → Dashboard**

This repository contains two versions:

1. **ETL Pipeline Demo** — works with a fixed/sample dataset.
2. **ETL Pipeline Live** — works with continuously generated/API-based order data.

---

## 📁 Repository Structure

```text
HelloQ_ETL_Pipeline/
│
├── README.md
├── etl_pipeline_demo/
│   ├── data/
│   ├── sql/
│   ├── src/
│   ├── tests/
│   └── requirements.txt
│
└── etl_pipeline_live/
    ├── api/
    │   └── app.py
    ├── dashboard/
    ├── data/
    ├── sql/
    ├── src/
    │   ├── analytics/
    │   ├── cleaning/
    │   ├── extract/
    │   ├── load/
    │   ├── transformation/
    │   └── validation/
    ├── tests/
    ├── .env.example
    ├── .gitignore
    ├── app.py
    └── requirements.txt
```

## 1️⃣ ETL Pipeline Demo

The demo uses a fixed/sample food-delivery dataset to learn and test the complete ETL process.

```text
Sample Dataset
      ↓
   Extract
      ↓
  Validate
      ↓
    Clean
      ↓
 Transform
      ↓
   Storage
      ↓
SQL Analytics
      ↓
 Dashboard
```

It covers data extraction, validation, cleaning, transformation, SQL analysis, business KPIs, and visualization.

Example business questions:

- How many orders were received?
- What is total revenue?
- What is average order value?
- Which city has the most orders?
- Which restaurant category is most popular?
- What is the cancellation rate?
- What is average delivery time?

## 2️⃣ ETL Pipeline Live

The live project takes the demo closer to a real-world Data Engineering system. It uses an API/live-data simulator to provide new order data and processes new batches incrementally.

```text
             API
              ↓
        New Order Data
              ↓
           Extract
              ↓
          Validate
          ↙       ↘
       Valid     Invalid
         ↓          ↓
       Clean     Rejected
         ↓
     Transform
         ↓
     PostgreSQL
         ↓
    SQL Analytics
         ↓
 Streamlit Dashboard
```

### Main ETL stages

**Extract**

```text
src/extract/extract_api.py
src/extract/live_data_simulator.py
```

**Validate**

Checks required fields, order IDs, amounts, status, timestamps, and data quality.

**Clean**

```text
src/cleaning/clean.py
```

Handles duplicates, missing values, data types, and standardization.

**Transform**

```text
src/transformation/transform.py
```

Creates analytical fields such as:

```text
net_amount
order_date
order_hour
order_day
is_delivered
is_cancelled
delivery_performance
```

**Load**

```text
src/load/load_postgres.py
```

Loads transformed records into PostgreSQL.

## ♻️ Incremental Processing

New batches can be added without unnecessarily reprocessing existing data.

```text
Batch 1 → 50 orders → PostgreSQL
Batch 2 → 10 new orders → PostgreSQL
Total   → 60 orders
```

Duplicate orders are prevented using `order_id`.

Runtime state is kept locally and is not uploaded to GitHub.

## 🗄️ PostgreSQL

Main table:

```text
orders
```

Example fields:

```text
order_id
customer_id
restaurant_id
order_timestamp
city
restaurant_category
order_status
payment_method
delivery_type
order_amount
discount
delivery_fee
net_amount
rating
delivery_time_minutes
delivery_performance
```

PostgreSQL provides persistent storage for the processed order data.

## 📊 SQL Analytics

Example queries:

```sql
SELECT COUNT(*) FROM orders;
```

```sql
SELECT SUM(net_amount) FROM orders;
```

```sql
SELECT AVG(net_amount) FROM orders;
```

```sql
SELECT city, COUNT(*) AS total_orders
FROM orders
GROUP BY city
ORDER BY total_orders DESC;
```

```sql
SELECT city, SUM(net_amount) AS total_revenue
FROM orders
GROUP BY city
ORDER BY total_revenue DESC;
```

```sql
SELECT restaurant_category, COUNT(*) AS total_orders
FROM orders
GROUP BY restaurant_category
ORDER BY total_orders DESC;
```

## 📈 Streamlit Dashboard

The live dashboard reads analytical data from PostgreSQL.

KPIs include:

- Total Orders
- Total Revenue
- Average Order Value
- Cancellation Rate
- Average Delivery Time

Charts include:

- Orders by City
- Revenue by City
- Restaurant Categories
- Order Status
- Payment Methods
- Orders by Hour
- Delivery Performance
- Delivery Types

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | ETL and application logic |
| Pandas | Data processing |
| API | Live data source |
| PostgreSQL | Data storage |
| psycopg2 | PostgreSQL connection |
| SQL | Analytics |
| Streamlit | Dashboard |
| Plotly | Visualization |
| Pytest | Testing |
| Git | Version control |
| GitHub | Code repository |

## 🧪 Testing

Run all tests:

```bash
pytest -v
```

Run validation tests:

```bash
pytest tests/test_validation.py -v
```

## 🔐 Environment Variables

Use a local `.env` file for database credentials.

Example:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=food_delivery
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

Never upload `.env`, passwords, API keys, or tokens to GitHub. Commit only `.env.example`.

## 🚫 Data Files

The live project does not upload generated/live data files to GitHub.

Keep these local:

```text
.env
*.csv
*.log
data/state/
api/order_id.txt
venv/
```

GitHub stores source code, SQL, tests, configuration templates, and documentation. Actual live data is stored in PostgreSQL.

## ▶️ Running the Live Project

Go to the live project:

```powershell
cd etl_pipeline_live
```

Activate the environment:

```powershell
.env\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
python api/app.py
```

Run the complete ETL:

```bash
python -m src.pipeline
```

Run the dashboard:

```bash
streamlit run app.py
```

## 🔄 Complete Workflow

```text
API
 ↓
Extract
 ↓
Validate
 ↓
Clean
 ↓
Transform
 ↓
PostgreSQL
 ↓
SQL Analytics
 ↓
Streamlit
 ↓
Dashboard
```

The current system demonstrates near-real-time/manual refresh. Automatic scheduling and streaming are future improvements.

## 📌 Demo vs Live

| Feature | Demo | Live |
|---|---|---|
| Sample Data | ✅ | ❌ |
| API Data | ❌ | ✅ |
| ETL | ✅ | ✅ |
| Validation | ✅ | ✅ |
| Cleaning | ✅ | ✅ |
| Transformation | ✅ | ✅ |
| PostgreSQL | Development | ✅ |
| Incremental Processing | Basic | ✅ |
| SQL Analytics | ✅ | ✅ |
| Dashboard | ✅ | ✅ |
| Live Data Simulation | ❌ | ✅ |

## 🚀 Future Improvements

- Automatic pipeline scheduling
- Automatic dashboard refresh
- Apache Airflow
- Apache Kafka
- Docker
- Data-quality monitoring
- Retry mechanisms
- Database optimization
- Customer analytics
- Restaurant analytics
- Real-time order monitoring
- Cloud deployment
- CI/CD

## 🏗️ Future Production Architecture

```text
Food Delivery Platform
         ↓
      API / Events
         ↓
       Kafka
         ↓
 Stream Processing
         ↓
     PostgreSQL
         ↓
   SQL Analytics
         ↓
 Streamlit / BI
         ↓
 Business Dashboard
```

## 🎓 What This Project Demonstrates

### Data Engineering
- ETL
- API ingestion
- Batch processing
- Incremental processing
- Data validation
- Data cleaning
- Data transformation
- PostgreSQL
- Data quality
- Duplicate prevention

### Data Analytics
- SQL
- Aggregations
- GROUP BY
- KPIs
- Revenue analysis
- Order analysis
- Delivery analysis

### Development
- Python
- Pandas
- REST API
- PostgreSQL
- Streamlit
- Plotly
- Pytest
- Git
- GitHub

## 📈 Project Status

### Demo

```text
ETL                     ✅
Validation              ✅
Cleaning                ✅
Transformation          ✅
SQL Analytics           ✅
Testing                 ✅
Dashboard               ✅
```

### Live

```text
API / Simulator         ✅
Extraction              ✅
Validation              ✅
Cleaning                ✅
Transformation          ✅
PostgreSQL              ✅
SQL Analytics           ✅
Dashboard               ✅
Incremental Processing  ✅
Automation              🔄
Automatic Refresh       🔄
Kafka                   📋 Planned
Airflow                 📋 Planned
Docker                  📋 Planned
Cloud                   📋 Planned
```

## 👩‍💻 Author

**Siddhi**

Data Engineering & Data Analytics Practice Project

## 📄 License

This project is created for educational, learning, and portfolio purposes.
