
def explain_recommendation(selected_movie, recommended_movie):
    """
    Explain why a movie was recommended using
    shared genres, cast, directors, and content similarity.
    """

    explanations = []

    # Compare genres
    selected_genres = set(
        selected_movie.get("genres") or []
    )

    recommended_genres = set(
        recommended_movie.get("genres") or []
    )

    shared_genres = sorted(
        selected_genres.intersection(recommended_genres)
    )

    if shared_genres:
        explanations.append(
            "Both movies share these genres: "
            + ", ".join(shared_genres)
        )

    # Compare cast
    selected_cast = set(
        selected_movie.get("cast") or []
    )

    recommended_cast = set(
        recommended_movie.get("cast") or []
    )

    shared_cast = sorted(
        selected_cast.intersection(recommended_cast)
    )

    if shared_cast:
        explanations.append(
            "They feature some of the same actors: "
            + ", ".join(shared_cast[:3])
        )

    # Compare directors
    selected_directors = set(
        selected_movie.get("directors") or []
    )

    recommended_directors = set(
        recommended_movie.get("directors") or []
    )

    shared_directors = sorted(
        selected_directors.intersection(
            recommended_directors
        )
    )

    if shared_directors:
        explanations.append(
            "Both movies were directed by "
            + ", ".join(shared_directors)
        )

    # Explain content similarity
    content_score = recommended_movie.get(
        "similarity_score",
        0
    )

    if content_score >= 0.3:
        explanations.append(
            "Their movie descriptions and content "
            "features show strong similarity."
        )

    elif content_score >= 0.15:
        explanations.append(
            "Their movie descriptions and content "
            "features show some similarity."
        )

    # Explain sentiment contribution
    sentiment_similarity = recommended_movie.get(
        "sentiment_similarity",
        0
    )

    if sentiment_similarity >= 0.8:
        explanations.append(
            "Their plot descriptions have similar "
            "sentiment scores."
        )

    if not explanations:
        explanations.append(
            "This movie was selected based on its "
            "combined content and sentiment ranking."
        )

    return explanations