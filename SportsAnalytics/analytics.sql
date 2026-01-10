
--Which teams have maintained Top 5 rankings across multiple seasons?
SELECT
	t.team_name,
	r.season_year, 
	COUNT(*) AS top5_weeks_total
FROM rankings r
JOIN teams t ON r.team_id = t.team_id
WHERE r.rank <= 5
GROUP BY t.team_name, r.season_year
HAVING COUNT(*) > 1
ORDER BY t.team_name, r.season_year;


-- What are the average ranking points per team by season?

SELECT
	t.team_name,
	r.season_year,
	ROUND(AVG(r.points),2) as avg_points
FROM rankings r
JOIN teams t on r.team_id = t.team_id
GROUP BY t.team_name,r.season_year
ORDER BY r.season_year,avg_points DESC;

-- How many first-place votes did each team receive across weeks?
select * from rankings limit 2;

SELECT
	t.team_name ,
	SUM(r.fp_votes) as total_first_place_votes
FROM rankings r
JOIN teams t ON r.team_id = t.team_id
GROUP BY t.team_name
ORDER BY total_first_place_votes DESC;

select * from players limit 2;
-- Which players have appeared in multiple seasons for the same team?
SELECT 
	p.first_name, 
	p.last_name, 
	t.team_name,
	COUNT(DISTINCT r.season_year) AS seasons_played
FROM players p
JOIN rankings r ON p.team_id = r.team_id
JOIN teams t ON r.team_id = t.team_id
GROUP BY p.first_name, p.last_name, t.team_name
HAVING COUNT(DISTINCT r.season_year) > 1
ORDER BY seasons_played DESC;

-- What are the most common player positions and their distribution across teams?
SELECT 
	t.team_name, 
	p.position, 
	COUNT(*) AS position_count
FROM players p
JOIN teams t ON p.team_id = t.team_id
GROUP BY t.team_name, p.position
ORDER BY t.team_name, position_count DESC;

