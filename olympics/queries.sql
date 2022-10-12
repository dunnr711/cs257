SELECT nocs.abbreviation, nocs.country FROM nocs
ORDER BY nocs.abbreviation;

SELECT DISTINCT athletes.first_name, athletes.last_name, nocs.country
FROM athletes, nocs, linked_master
WHERE athletes.id = linked_master.athlete_id
AND nocs.id = linked_master.nocs_id
AND nocs.country = 'Jamaica'
ORDER BY athletes.last_name;

SELECT  athletes.first_name, athletes.last_name, medals.medal, nocs.country, olympic_games.year, olympic_games.season
FROM athletes, medals, olympic_games, nocs, linked_master
WHERE athletes.id = linked_master.athlete_id
AND medals.id = linked_master.medals_id
AND olympic_games.id = linked_master.olympic_games
AND nocs.id = linked_master.nocs_id
AND medals.medal not in ('NA')
AND athletes.first_name = 'Gregory'
AND athletes.last_name = 'Louganis'
ORDER BY olympic_games.year;


SELECT COUNT (medals.medal), nocs.country
FROM nocs, medals, linked_master
WHERE medals.id = linked_master.medals_id
AND nocs.id = linked_master.nocs_id
AND medals.medal = 'Gold'
GROUP BY nocs.country
ORDER BY COUNT(medals.id) DESC;