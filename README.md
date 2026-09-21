# 📊 Data Analyst Job Market Analyzer – India

An end-to-end data analytics project analyzing job-market demand across India using job postings collected through the **Adzuna API**.

The project combines **Python, SQL, MySQL, Power BI, and DAX** to collect, clean, transform, analyze, and visualize job-market data across skills, cities, industries, and salary levels.

---

## 🎯 Project Objective

The objective of this project is to understand the Indian Data Analyst job market by answering questions such as:

- Which cities have the highest job-posting volume?
- Which skills are most in demand?
- Which skills commonly appear together?
- Which industries have the highest number of job postings?
- How are salaries distributed across different salary bands?
- How do average salaries vary across industries?

---

## 📡 Data Collection

Instead of relying on a pre-existing Kaggle dataset, job postings were collected through the **Adzuna API** using Python.

### Data Collection Summary

| Metric | Value |
|---|---:|
| Job postings collected | 2,020+ |
| Unique postings after deduplication | 1,878 |
| Cities analyzed | 8 |
| Target skills extracted | 14 |
| Skill-posting associations | 887 |

### Cities Covered

- Bangalore
- Chennai
- Coimbatore
- Delhi
- Hyderabad
- Kolkata
- Mumbai
- Pune

---

## 🛠️ Tools & Technologies

- **Python** – API data collection, data processing, skill extraction
- **SQL** – Data analysis and querying
- **MySQL** – Relational data storage
- **Power BI** – Interactive dashboard and visualization
- **DAX** – Measures and analytical calculations
- **Power Query** – Data transformation
- **Regex** – Skill extraction from unstructured job descriptions
- **Git/GitHub** – Version control and project documentation

---


## 🔄 Project Workflow

```text
Adzuna API
    ↓
Python Data Collection
    ↓
Data Cleaning & Deduplication
    ↓
SQLite / MySQL
    ↓
SQL Analysis
    ↓
Python Skill Extraction
    ↓
Power BI Data Model
    ↓
DAX Measures
    ↓
Interactive Dashboard
    ↓
Business Insights

## 🐍 Python Data Processing

Python was used to:

- Collect job postings through the Adzuna API
- Process and clean raw API responses
- Remove duplicate job postings
- Extract skills from unstructured job descriptions
- Create skill-posting relationships
- Prepare data for SQL and Power BI analysis

A regex-based skill-extraction pipeline identified **14 target skills**, generating **887 skill-posting associations**.

---

## 🗄️ SQL & MySQL Analysis

The cleaned job-posting data was stored in a relational MySQL database.

SQL analysis included:

- `JOIN`
- `GROUP BY`
- Aggregations
- Subqueries
- `CASE` statements
- `HAVING`
- Window functions
- `RANK() OVER()`

The analysis focused on:

- Skill demand
- City-level hiring concentration
- Industry distribution
- Salary distribution
- Skill relationships

---

## 🧠 Skill Demand Analysis

The analysis identified **SQL as the most frequently occurring extracted skill**, followed by Python.

### Top Skills

| Skill | Postings |
|---|---:|
| SQL | 163 |
| Python | 98 |
| Communication | 89 |
| Excel | 77 |
| Power BI | 75 |
| Machine Learning | 68 |
| Statistics | 68 |
| ETL | 60 |
| Tableau | 52 |
| Azure | 43 |

SQL appeared in approximately **8.7%** of the analyzed postings, while Python appeared in approximately **5.2%**.

Among postings requiring Python, approximately **61% also required SQL**, making SQL the strongest observed co-occurring skill with Python in this dataset.

---

## 📊 Power BI Dashboard

The final Power BI dashboard contains **3 pages**.

### 1. Overview

Provides a high-level view of:

- Total job postings
- Companies hiring
- Cities covered
- Top companies
- Job postings by city
- Top skills in demand

### 2. Skills Demand & Co-occurrence Analysis

Analyzes:

- Skill demand across cities
- Python skill co-occurrence
- Average extracted skills per posting by city

### 3. Industry & Compensation Analysis

Analyzes:

- Job postings by industry
- Salary bands
- Average salary by industry
- Salary disclosure levels

For the industry salary comparison, categories with fewer than **5 salary-disclosed postings** were excluded to reduce small-sample distortion.

---

## 💡 Key Insights

- **SQL** was the most frequently occurring extracted skill in the dataset.
- **Python and SQL** showed a strong co-occurrence relationship.
- Job postings were concentrated across major Indian cities, with Bangalore representing the largest share in the analyzed dataset.
- **1,499 of 1,878 postings did not disclose salary**, limiting salary-based analysis.
- Among industries with at least **5 salary-disclosed postings**, average salaries ranged from approximately **₹8.4L to ₹14.7L**.
- Skill requirements varied across cities, highlighting differences in local job-market demand.

---

## 🔍 Data Validation

An important part of this project was validating the dashboard metrics against the underlying data model.

During development, a discrepancy was identified between job-posting counts and skill-level records.

The project contains two related concepts:


The project contains two related concepts:

`postings[id]`  
↓  
`posting_skills[posting_id]`

```
📸 Dashboard Screenshots

Overview
![Overview Dashboard](screenshots/overview.png)
Skills Demand & Co-occurrence Analysis
![Skills Demand Dashboard](screenshots/skills-demand.png)
Industry & Compensation Analysis
![Industry & Compensation Dashboard](screenshots/industry-compensation.png)

👤 Author

Bala Hariharan B

Aspiring Data Analyst | Python | SQL | Power BI | Excel

📍 Chennai, India

