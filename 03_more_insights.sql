USE job_market_analyzer;

-- 1. Skill demand matrix: top 5 skills, broken down by city
SELECT
    p.city_query,
    ps.skill,
    COUNT(*) AS mentions
FROM posting_skills ps
JOIN postings p ON ps.posting_id = p.id
WHERE ps.skill IN ('SQL', 'Python', 'Excel', 'Power BI', 'Communication')
GROUP BY p.city_query, ps.skill
ORDER BY p.city_query, mentions DESC;

-- 2. Category / role-type breakdown
SELECT
    category,
    COUNT(*) AS postings,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM postings), 1) AS pct_of_total
FROM postings
WHERE category IS NOT NULL
GROUP BY category
ORDER BY postings DESC;

-- 3. Salary bands (rough buckets) among postings with salary data
SELECT
    CASE
        WHEN salary_max < 500000 THEN 'Under 5L'
        WHEN salary_max < 1000000 THEN '5L - 10L'
        WHEN salary_max < 1500000 THEN '10L - 15L'
        WHEN salary_max < 2000000 THEN '15L - 20L'
        ELSE '20L+'
    END AS salary_band,
    COUNT(*) AS postings
FROM postings
WHERE salary_max IS NOT NULL
GROUP BY salary_band
ORDER BY MIN(salary_max);

-- 4. Postings over time (by month, using created date)
SELECT
    DATE_FORMAT(created, '%Y-%m') AS month,
    COUNT(*) AS postings
FROM postings
WHERE created IS NOT NULL
GROUP BY month
ORDER BY month;

-- 5. Search term breakdown by city (which cities lean more "business analyst" vs "data analyst")
SELECT
    city_query,
    search_term,
    COUNT(*) AS postings
FROM postings
GROUP BY city_query, search_term
ORDER BY city_query, postings DESC;
