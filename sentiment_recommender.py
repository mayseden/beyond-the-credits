
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def calculate_sentiment(text):
    """Calculate the sentiment of a movie description."""
    if not text or not text.strip():
        return 0.0

    scores = analyzer.polarity_scores(text)
    return round(scores["compound"], 4)


def recommend_by_sentiment(movie_title, movies, top_n=5):
    """Recommend movies using plot sentiment and genre relevance."""

    selected_movie = next(
        (
            movie for movie in movies
            if movie["title"].lower() == movie_title.lower()
        ),
        None
    )

    if selected_movie is None:
        return []

    selected_sentiment = calculate_sentiment(
        selected_movie.get("overview", "")
    )

    selected_genres = set(
        selected_movie.get("genres", [])
    )

    recommendations = []

    for movie in movies:
        if movie["id"] == selected_movie["id"]:
            continue

        movie_sentiment = calculate_sentiment(
            movie.get("overview", "")
        )

        sentiment_similarity = 1 - (
            abs(selected_sentiment - movie_sentiment) / 2
        )

        movie_genres = set(movie.get("genres", []))

        if selected_genres or movie_genres:
            genre_similarity = (
                len(selected_genres & movie_genres)
                / len(selected_genres | movie_genres)
            )
        else:
            genre_similarity = 0.0

        combined_score = (
            0.75 * sentiment_similarity
            + 0.25 * genre_similarity
        )

        result = movie.copy()
        result["sentiment_score"] = movie_sentiment
        result["sentiment_similarity"] = round(
            sentiment_similarity, 4
        )
        result["genre_similarity"] = round(
            genre_similarity, 4
        )
        result["sentiment_recommendation_score"] = round(
            combined_score, 4
        )

        recommendations.append(result)

    recommendations.sort(
        key=lambda movie: movie[
            "sentiment_recommendation_score"
        ],
        reverse=True
    )

    return recommendations[:top_n]