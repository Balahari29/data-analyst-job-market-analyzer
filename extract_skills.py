"""
Extract skill mentions from job descriptions and store results in MySQL.
-----------------------------------------------------------------------
Reads every row from `postings`, scans the description text for a fixed
list of skill keywords, and writes matches into a new `posting_skills` table
(one row per posting-skill pair).

Setup:
    pip install mysql-connector-python

Run this AFTER migrate_to_mysql.py has populated the postings table.

Usage:
    python extract_skills.py
"""

import mysql.connector
import re

# ---- MySQL connection — same as migrate_to_mysql.py ----
MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "211620",  # <-- change this
    "database": "job_market_analyzer",
}

# ---- Skills to search for ----
# key = clean skill name to store, value = list of text patterns that count as a match
SKILLS = {
    "Python": [r"\bpython\b"],
    "SQL": [r"\bsql\b", r"\bmysql\b", r"\bpostgresql\b"],
    "Power BI": [r"\bpower ?bi\b"],
    "Excel": [r"\bexcel\b", r"\bvlookup\b", r"\bpivot table"],
    "Tableau": [r"\btableau\b"],
    "R": [r"\br programming\b", r"\br studio\b"],
    "Machine Learning": [r"\bmachine learning\b", r"\bml\b"],
    "Statistics": [r"\bstatistic", r"\bregression\b"],
    "Data Visualization": [r"\bdata visuali[sz]ation\b"],
    "ETL": [r"\betl\b"],
    "Spark": [r"\bspark\b", r"\bpyspark\b"],
    "AWS": [r"\baws\b", r"\bamazon web services\b"],
    "Azure": [r"\bazure\b"],
    "Communication": [r"\bcommunication skills\b", r"\bstakeholder\b"],
}

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS posting_skills (
    posting_id VARCHAR(64),
    skill VARCHAR(100),
    PRIMARY KEY (posting_id, skill)
)
"""


def find_skills_in_text(text):
    """Return the list of skill names whose patterns match somewhere in the text."""
    if not text:
        return []
    text_lower = text.lower()
    found = []
    for skill_name, patterns in SKILLS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                found.append(skill_name)
                break  # no need to check other patterns for this skill
    return found


def main():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cur = conn.cursor()

    cur.execute(CREATE_TABLE_SQL)
    conn.commit()

    cur.execute("SELECT id, description FROM postings")
    rows = cur.fetchall()
    print(f"Scanning {len(rows)} postings for skill mentions...")

    insert_cur = conn.cursor()
    total_matches = 0

    for posting_id, description in rows:
        skills_found = find_skills_in_text(description)
        for skill in skills_found:
            try:
                insert_cur.execute(
                    "INSERT IGNORE INTO posting_skills (posting_id, skill) VALUES (%s, %s)",
                    (posting_id, skill)
                )
                total_matches += 1
            except Exception as e:
                print(f"  [!] Failed on {posting_id} / {skill}: {e}")

    conn.commit()
    insert_cur.close()
    cur.close()
    conn.close()

    print(f"Done. Inserted {total_matches} posting-skill matches into posting_skills.")


if __name__ == "__main__":
    main()
