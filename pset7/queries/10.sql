/* write a SQL query to list the names of all people who have directed a movie that received a rating of at least 9.0. */ 
SELECT name 
From people
WHERE id IN (  
    SELECT directors.person_id
    FROM directors
    JOIN ratings ON directors.movie_id = ratings.movie_id
    WHERE ratings.rating >= 9 );