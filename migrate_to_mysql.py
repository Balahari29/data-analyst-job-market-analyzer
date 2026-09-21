"""
Migrate job postings from SQLite (jobs.db) into MySQL.
-----------------------------------------------------------
Run this AFTER collect_jobs.py has created jobs.db.

Setup:
    pip install mysql-connector-python

Before running, create the target database in MySQL Workbench:
    CREATE DATABASE job_market_analyzer;

Fill in your MySQL connection details below, then run:
    python migrate_to_mysql.py
"""

import sqlite3
import mysql.connector

# ---- SQLite source ----
SQLITE_DB_PATH = "jobs.db"

# ---- MySQL destination — EDIT THESE ----
MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",  # <-- change this
    "database": "job_market_analyzer",
}


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS postings (
    id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(500),
    company VARCHAR(255),
    location VARCHAR(255),
    city_query VARCHAR(100),
    search_term VARCHAR(100),
    salary_min FLOAT,
    salary_max FLOAT,
    category VARCHAR(255),
    created DATETIME NULL,
    description TEXT,
    redirect_url VARCHAR(1000),
    collected_at DATETIME NULL
)
"""

INSERT_SQL = """
INSERT IGNORE INTO postings
(id, title, company, location, city_query, search_term,
 salary_min, salary_max, category, created, description,
 redirect_url, collected_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


def clean_datetime(value):
    """Adzuna dates come like '2026-08-01T09:30:00Z' — MySQL DATETIME wants 'YYYY-MM-DD HH:MM:SS'."""
    if not value:
        return None
    return value.replace("T", " ").replace("Z", "").split(".")[0]


def main():
    # --- read from SQLite ---
    sconn = sqlite3.connect(SQLITE_DB_PATH)
    sconn.row_factory = sqlite3.Row
    rows = sconn.execute("SELECT * FROM postings").fetchall()
    sconn.close()
    print(f"Read {len(rows)} rows from SQLite.")

    # --- connect to MySQL ---
    mconn = mysql.connector.connect(**MYSQL_CONFIG)
    mcur = mconn.cursor()
    mcur.execute(CREATE_TABLE_SQL)
    mconn.commit()

    inserted = 0
    for r in rows:
        try:
            mcur.execute(INSERT_SQL, (
                r["id"], r["title"], r["company"], r["location"],
                r["city_query"], r["search_term"],
                r["salary_min"], r["salary_max"], r["category"],
                clean_datetime(r["created"]),
                r["description"], r["redirect_url"],
                clean_datetime(r["collected_at"]),
            ))
            inserted += 1
        except Exception as e:
            print(f"  [!] Failed on row {r['id']}: {e}")

    mconn.commit()
    mcur.close()
    mconn.close()
    print(f"Inserted {inserted} rows into MySQL database '{MYSQL_CONFIG['database']}'.")


if __name__ == "__main__":
    main()
