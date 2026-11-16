import numpy as np
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_from_watchlist(watchlist_ids, movies, top_n=5):
    """
    Recommend movies based on a user's saved watchlist.

    Uses a TF-IDF profile built from the content of
    saved movies and ranks unseen movies by similarity.
    """

    if not watchlist_ids or not movies:
        return []

    saved_ids = set(watchlist_ids)

    saved_movies = [
        movie for movie in movies
        if movie.get("id") in saved_ids
    ]

    if not saved_movies:
        return []

    # Build a text representation of each movie
    documents = []

    for movie in movies:
        combined_text = movie.get("combined_text") or ""

        if not combined_text.strip():
            combined_text = (
                (movie.get("overview") or "")
                + " "
                + " ".join(movie.get("genres") or [])
            )

        documents.append(combined_text)

    if not any(document.strip() for document in documents):
        return []

    # Create TF-IDF movie vectors
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000,
        ngram_range=(1, 2)
    )

    movie_vectors = vectorizer.fit_transform(documents)

    # Find the indices of saved movies
    saved_indices = [
        index for index, movie in enumerate(movies)
        if movie.get("id") in saved_ids
    ]

    # Average saved movie vectors to build a user profile
    profile_vector = np.asarray(
    movie_vectors[saved_indices].mean(axis=0)
)

    # Compare the user profile against all movies
    similarities = cosine_similarity(
        profile_vector,
        movie_vectors
    ).flatten()

    # Identify the user's most common genres
    genre_counts = Counter(
        genre
        for movie in saved_movies
        for genre in (movie.get("genres") or [])
    )

    favourite_genres = [
        genre
        for genre, _ in genre_counts.most_common(3)
    ]

    recommendations = []

    for index, movie in enumerate(movies):

        if movie.get("id") in saved_ids:
            continue

        score = float(similarities[index])

        if score <= 0:
            continue

        result = movie.copy()
        result["profile_similarity_score"] = round(score, 4)

        result["shared_profile_genres"] = [
            genre
            for genre in (movie.get("genres") or [])
            if genre in favourite_genres
        ]

        recommendations.append(result)

    recommendations.sort(
        key=lambda movie: movie["profile_similarity_score"],
        reverse=True
    )

    return recommendations[:top_n]