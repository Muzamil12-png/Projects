SELECT DISTINCT m.title
FROM movies m
WHERE m.id IN (
    SELECT s1.movie_id
    FROM stars s1
    JOIN stars s2 ON s1.movie_id = s2.movie_id
    JOIN people p1 ON s1.person_id = p1.id
    JOIN people p2 ON s2.person_id = p2.id
    WHERE p1.name = 'Bradley Cooper' AND p2.name = 'Jennifer Lawrence'
);
