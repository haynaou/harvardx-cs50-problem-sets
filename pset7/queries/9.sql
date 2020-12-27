/* write a SQL query to list the names of all people who starred in a movie released in 2004, ordered by birth year */
SELECT name 
From people
WHERE id in ( 
    SELECT stars.person_id
    FROM stars
    JOIN movies on movies.id = stars.movie_id
    WHERE movies.year = 2004)
ORDER BY birth;