
from recommender import recommend_by_content
from sentiment_recommender import recommend_by_sentiment


def recommend_hybrid(movie_title, movies, top_n=5):
    """Combine content-based and sentiment-based recommendations."""

    if not any(
        movie["title"].lower() == movie_title.lower()
        for movie in movies
    ):
        return []

    content_results = recommend_by_content(
        movie_title, movies, top_n=len(movies)
    )

    sentiment_results = recommend_by_sentiment(
        movie_title, movies, top_n=len(movies)
    )

    content_lookup = {
        movie["id"]: movie
        for movie in content_results
    }

    sentiment_lookup = {
        movie["id"]: movie
        for movie in sentiment_results
    }

    recommendations = []

    for movie_id, content_movie in content_lookup.items():
        sentiment_movie = sentiment_lookup.get(movie_id)

        if sentiment_movie is None:
            continue

        content_score = content_movie["similarity_score"]

        sentiment_score = sentiment_movie[
            "sentiment_recommendation_score"
        ]

        hybrid_score = (
            0.70 * content_score
            + 0.30 * sentiment_score
        )

        result = content_movie.copy()

        result["sentiment_score"] = sentiment_movie[
            "sentiment_score"
        ]
        result["sentiment_similarity"] = sentiment_movie[
            "sentiment_similarity"
        ]
        result["genre_similarity"] = sentiment_movie[
            "genre_similarity"
        ]
        result["sentiment_recommendation_score"] = (
            sentiment_score
        )
        result["hybrid_score"] = round(hybrid_score, 4)

        recommendations.append(result)

    recommendations.sort(
        key=lambda movie: movie["hybrid_score"],
        reverse=True
    )

    return recommendations[:top_n]