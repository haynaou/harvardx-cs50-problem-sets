/*  write a SQL query to list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated */
SELECT title 
FROM movies
WHERE id IN (
    SELECT  ratings.movie_id
    FROM ratings
    WHERE ratings.movie_id IN (
        SELECT stars.movie_id
        FROM stars
        JOIN people ON people.id = stars.person_id
        WHERE people.name = 'Chadwick Boseman')
    ORDER BY ratings.rating DESC 
    LIMIT 5);