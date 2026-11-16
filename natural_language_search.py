
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def search_movies_by_description(query, movies, top_n=5):
    """
    Find movies matching a natural-language description
    using TF-IDF and cosine similarity.
    """

    if not query or not query.strip():
        return []

    if not movies:
        return []

    # Combine searchable movie information
    movie_documents = []

    for movie in movies:

        overview = movie.get("overview") or ""

        genres = " ".join(
            movie.get("genres") or []
        )

        keywords = movie.get("keywords") or []

        if isinstance(keywords, list):
            keyword_text = " ".join(
                str(keyword) for keyword in keywords
            )
        else:
            keyword_text = str(keywords)

        combined_text = (
            f"{overview} {genres} {keyword_text}"
        )

        movie_documents.append(combined_text)

    # Include the user's query in the same TF-IDF space
    documents = movie_documents + [query.strip()]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    # Compare the query against every movie
    query_vector = tfidf_matrix[-1]

    movie_vectors = tfidf_matrix[:-1]

    similarity_scores = cosine_similarity(
        query_vector,
        movie_vectors
    ).flatten()

    ranked_indices = similarity_scores.argsort()[::-1]

    recommendations = []

    for index in ranked_indices:

        score = float(similarity_scores[index])

        # Ignore movies with no textual similarity
        if score <= 0:
            continue

        movie = movies[index].copy()

        movie["query_similarity_score"] = round(
            score,
            4
        )

        recommendations.append(movie)

        if len(recommendations) >= top_n:
            break

    return recommendations