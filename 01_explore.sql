USE job_market_analyzer;

-- 1. Total postings and basic sanity check
SELECT COUNT(*) AS total_postings FROM postings;

-- 2. Postings by city
SELECT city_query, COUNT(*) AS postings
FROM postings
GROUP BY city_query
ORDER BY postings DESC;

-- 3. Postings by search term (data analyst / data analytics / business analyst)
SELECT search_term, COUNT(*) AS postings
FROM postings
GROUP BY search_term
ORDER BY postings DESC;

-- 4. How many postings actually have salary data?
SELECT
    COUNT(*) AS total,
    SUM(CASE WHEN salary_min IS NOT NULL THEN 1 ELSE 0 END) AS with_salary,
    ROUND(SUM(CASE WHEN salary_min IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_with_salary
FROM postings;

-- 5. Top companies by number of postings
SELECT company, COUNT(*) AS postings
FROM postings
WHERE company IS NOT NULL
GROUP BY company
ORDER BY postings DESC
LIMIT 15;

-- 6. Average salary range by city (only where salary data exists)
SELECT
    city_query,
    COUNT(*) AS postings_with_salary,
    ROUND(AVG(salary_min), 0) AS avg_salary_min,
    ROUND(AVG(salary_max), 0) AS avg_salary_max
FROM postings
WHERE salary_min IS NOT NULL
GROUP BY city_query
ORDER BY avg_salary_max DESC;

-- 7. Sample a few titles to sanity-check data quality
SELECT title, company, location, created
FROM postings
ORDER BY created DESC
LIMIT 10;

