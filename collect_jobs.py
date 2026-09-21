
"""
Data Analyst Job Market Analyzer — Data Collection Script
-----------------------------------------------------------
Pulls Data Analyst job postings across major Indian cities using the
Adzuna Jobs API and saves them to a local SQLite database + raw JSON backups.

Setup:
    pip install requests

Usage:
    python collect_jobs.py
"""

import requests
import sqlite3
import json
import time
import os
from datetime import datetime

# ---- YOUR ADZUNA CREDENTIALS ----
APP_ID = "f79a552d"
APP_KEY = "22283b04a56a0e5a33766446a9da01b4"

# ---- CONFIG ----
COUNTRY = "in"  # India
SEARCH_TERMS = ["data analyst", "data analytics", "business analyst"]
CITIES = [
    "Chennai", "Bangalore", "Mumbai", "Hyderabad",
    "Pune", "Delhi", "Coimbatore", "Kolkata"
]
RESULTS_PER_PAGE = 50  # Adzuna max per page
MAX_PAGES_PER_QUERY = 2  # keep this low to conserve your 1000 calls/month
DB_PATH = "jobs.db"
RAW_DIR = "raw_responses"

BASE_URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS postings (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            city_query TEXT,
            search_term TEXT,
            salary_min REAL,
            salary_max REAL,
            category TEXT,
            created TEXT,
            description TEXT,
            redirect_url TEXT,
            collected_at TEXT
        )
    """)
    conn.commit()


def fetch_page(search_term, city, page):
    url = BASE_URL.format(country=COUNTRY, page=page)
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": RESULTS_PER_PAGE,
        "what": search_term,
        "where": city,
        "content-type": "application/json",
    }
    resp = requests.get(url, params=params, timeout=30)
    if resp.status_code != 200:
        print(f"  [!] Error {resp.status_code} for {search_term} / {city} page {page}: {resp.text[:200]}")
        return None
    return resp.json()


def save_raw(data, search_term, city, page):
    os.makedirs(RAW_DIR, exist_ok=True)
    fname = f"{RAW_DIR}/{search_term.replace(' ', '_')}_{city}_{page}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def insert_postings(conn, data, search_term, city):
    if not data or "results" not in data:
        return 0
    count = 0
    now = datetime.utcnow().isoformat()
    for job in data["results"]:
        try:
            conn.execute("""
                INSERT OR IGNORE INTO postings
                (id, title, company, location, city_query, search_term,
                 salary_min, salary_max, category, created, description,
                 redirect_url, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job.get("id"),
                job.get("title"),
                (job.get("company") or {}).get("display_name"),
                (job.get("location") or {}).get("display_name"),
                city,
                search_term,
                job.get("salary_min"),
                job.get("salary_max"),
                (job.get("category") or {}).get("label"),
                job.get("created"),
                job.get("description"),
                job.get("redirect_url"),
                now,
            ))
            count += 1
        except Exception as e:
            print(f"  [!] Failed to insert job: {e}")
    conn.commit()
    return count


def main():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    total_inserted = 0
    total_calls = 0

    for search_term in SEARCH_TERMS:
        for city in CITIES:
            for page in range(1, MAX_PAGES_PER_QUERY + 1):
                print(f"Fetching: '{search_term}' in {city}, page {page}...")
                data = fetch_page(search_term, city, page)
                total_calls += 1

                if data is None:
                    continue

                save_raw(data, search_term, city, page)
                inserted = insert_postings(conn, data, search_term, city)
                total_inserted += inserted
                print(f"  -> {inserted} postings inserted (this page)")

                # stop paging early if fewer results than a full page
                if len(data.get("results", [])) < RESULTS_PER_PAGE:
                    break

                time.sleep(1)  # be polite to the API

    conn.close()
    print(f"\nDone. Total API calls used: {total_calls}. Total postings inserted: {total_inserted}")
    print(f"Database saved to: {os.path.abspath(DB_PATH)}")


if __name__ == "__main__":
    main()
