SELECT AVG(energy) from songs Where artist_id in (Select id from artists WHERE name = 'Drake');

