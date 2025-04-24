SELECT AVG(rating) from ratings Join movies on ratings.movie_id = movies.id WHERE movies.year = 2012;
