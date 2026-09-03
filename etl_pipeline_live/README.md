# 🍔 Food Delivery Live ETL & Analytics Pipeline

A real-world style **Data Engineering + Analytics project** that demonstrates how live food-delivery order data can be extracted, validated, cleaned, transformed, stored in PostgreSQL, analyzed using SQL, and visualized through an interactive Streamlit dashboard.

The project is designed as a practice system for working with continuously arriving data.

---

## 📌 Project Overview

The pipeline simulates a food-delivery platform where new order data arrives through an API.

The system processes the incoming data through multiple ETL stages:

```text
Food Delivery API
       ↓
    Extract
       ↓
 Incoming Data
       ↓
   Validate
    ↙     ↘
 Valid   Rejected
   ↓
 Clean
   ↓
Transform
   ↓
PostgreSQL
   ↓
 SQL Analytics
   ↓
Streamlit Dashboard