
def filter_movies(
    movies,
    year_min=None,
    year_max=None,
    min_rating=None,
    min_votes=None,
    runtime_min=None,
    runtime_max=None,
    certification=None,
    language=None,
    actor=None,
    director=None,
    genres=None,
    genre_logic="OR"
):
    """Filter movies based on user preferences."""

    filtered = []

    for movie in movies:
        year = movie.get("release_year")
        rating = movie.get("rating") or 0
        votes = movie.get("vote_count") or 0
        runtime = movie.get("runtime") or 0

        if year_min is not None:
            if not year or year < year_min:
                continue

        if year_max is not None:
            if not year or year > year_max:
                continue

        if min_rating is not None and rating < min_rating:
            continue

        if min_votes is not None and votes < min_votes:
            continue

        if runtime_min is not None and runtime < runtime_min:
            continue

        if runtime_max is not None and runtime > runtime_max:
            continue

        if certification:
            if movie.get("certification", "").lower() != certification.lower():
                continue

        if language:
            if movie.get("original_language", "").lower() != language.lower():
                continue

        if actor:
            cast = movie.get("cast") or []
            if not any(actor.lower() in name.lower() for name in cast):
                continue

        if director:
            directors = movie.get("directors") or []
            if not any(
                director.lower() in name.lower()
                for name in directors
            ):
                continue

        if genres:
            movie_genres = {
                genre.lower() for genre in movie.get("genres", [])
            }
            requested_genres = {
                genre.lower() for genre in genres
            }

            if genre_logic.upper() == "AND":
                if not requested_genres.issubset(movie_genres):
                    continue
            else:
                if not requested_genres.intersection(movie_genres):
                    continue

        filtered.append(movie)

    return filtered