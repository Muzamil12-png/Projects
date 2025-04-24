SELECT DISTINCT name from people Where id in (
    Select person_id from directors
    Where movie_id in (
    Select id from movies JOIN ratings on movies.id = ratings.movie_id
    Where rating >= 9.0
    )
);

