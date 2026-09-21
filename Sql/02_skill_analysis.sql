USE job_market_analyzer;

-- 1. Overall skill frequency across all postings
SELECT
    skill,
    COUNT(*) AS mentions,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM postings), 1) AS pct_of_postings
FROM posting_skills
GROUP BY skill
ORDER BY mentions DESC;

-- 2. Top skills per city (using a JOIN)
SELECT
    p.city_query,
    ps.skill,
    COUNT(*) AS mentions
FROM posting_skills ps
JOIN postings p ON ps.posting_id = p.id
GROUP BY p.city_query, ps.skill
ORDER BY p.city_query, mentions DESC;

-- 3. Which skills tend to appear together (co-occurrence with Python)
SELECT
    ps2.skill AS paired_with_python,
    COUNT(*) AS co_occurrences
FROM posting_skills ps1
JOIN posting_skills ps2 ON ps1.posting_id = ps2.posting_id AND ps1.skill != ps2.skill
WHERE ps1.skill = 'Python'
GROUP BY ps2.skill
ORDER BY co_occurrences DESC;

-- 4. Average number of skills required per posting
SELECT
    ROUND(AVG(skill_count), 1) AS avg_skills_per_posting
FROM (
    SELECT posting_id, COUNT(*) AS skill_count
    FROM posting_skills
    GROUP BY posting_id
) AS per_posting_counts;

-- 5. Skill ranking using window function (RANK)
SELECT
    skill,
    COUNT(*) AS mentions,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS skill_rank
FROM posting_skills
GROUP BY skill;
