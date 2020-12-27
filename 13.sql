/* write a SQL query to list the names of all people who starred in a movie in which Kevin Bacon also starred.
select the Kevin Bacon who's born in 1958
Kevin Bacon himself should not be included in the resulting list */

SELECT DISTINCT people.name
FROM people 
JOIN stars ON stars.person_id = people.id 
WHERE stars.movie_id IN (
	SELECT  movie_id
	FROM stars 
	JOIN people ON people.id = stars.person_id
	WHERE (people.name = 'Kevin Bacon'  AND people.birth = 1958))
AND people.id NOT IN (
	SELECT people.id
	FROM people
	WHERE (people.name = 'Kevin Bacon'  AND people.birth = 1958));