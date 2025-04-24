SELECT n.name from people n JOIN stars s ON n.id = s.person_id JOIN movies k ON s.movie_id = k.id WHERE k.title = 'Toy Story';
