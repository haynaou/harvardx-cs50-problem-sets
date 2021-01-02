/* write a SQL query to list the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred. */ 
SELECT title
FROM movies 
WHERE id IN (
    SELECT stars.movie_id
    FROM stars
    JOIN people ON people.id = stars.person_id
    WHERE people.name = 'Helena Bonham Carter' 
    AND stars.movie_id IN (
        SELECT stars.movie_id
        FROM stars
        JOIN people ON people.id = stars.person_id
        WHERE people.name = 'Johnny Depp'));