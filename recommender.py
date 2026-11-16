
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_FILE = Path(__file__).resolve().parent / "data" / "movies.json"


def load_movies():
    """Load the processed movie dataset."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def build_content_model(movies):
    """Create TF-IDF vectors for movie content."""

    movie_texts = [
        movie.get("combined_text", "")
        for movie in movies
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000,
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(movie_texts)

    return vectorizer, tfidf_matrix


def recommend_by_content(movie_title, movies, top_n=5):
    """Recommend movies based on content similarity."""

    # Find the selected movie
    matching_indices = [
        index
        for index, movie in enumerate(movies)
        if movie["title"].lower() == movie_title.lower()
    ]

    if not matching_indices:
        return []

    selected_index = matching_indices[0]

    # Build the TF-IDF model
    _, tfidf_matrix = build_content_model(movies)

    # Calculate similarity with the selected movie
    similarity_scores = cosine_similarity(
        tfidf_matrix[selected_index],
        tfidf_matrix
    ).flatten()

    # Rank movies by similarity
    ranked_indices = similarity_scores.argsort()[::-1]

    recommendations = []

    for index in ranked_indices:
        # Don't recommend the same movie
        if index == selected_index:
            continue

        movie = movies[index].copy()

        movie["similarity_score"] = round(
            float(similarity_scores[index]), 4
        )

        recommendations.append(movie)

        if len(recommendations) >= top_n:
            break

    return recommendations