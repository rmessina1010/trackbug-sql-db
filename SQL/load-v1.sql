SELECT 
	COUNT(*), 
	CAST(AVG(bug_weight) AS DECIMAL(4,3)) , 
	SUM(bug_weight) as load, 
	assigned_to as dev 
FROM bugs
LEFT JOIN personel
ON person_id = assigned_to
WHERE assigned_to IS NULL
GROUP BY assigned_to 

--OR
WITH loadsTable AS
(SELECT COUNT(*), 
CAST(AVG(bug_weight) AS DECIMAL(4, 3)), 
SUM(bug_weight) as load, 
assigned_to as dev
FROM bugs
group by assigned_to)
SELECT count,avg, dev,first_name,last_name,reports_to,p_role,work_stat FROM loadsTable
LEFT JOIN personel ON personel.person_id = loadsTable.dev 