/* write a SQL query to list the names of all people who starred in Toy Story */
SELECT name 
FROM people 
WHERE id in (
    SELECT stars.person_id
    FROM movies
    JOIN stars on stars.movie_id = movies.id
    WHERE movies.title LIKE 'Toy Story');