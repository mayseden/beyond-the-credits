
from recommender import load_movies
from sentiment_recommender import (
    calculate_sentiment,
    recommend_by_sentiment
)

movies = load_movies()

print("\nBEYOND THE CREDITS - SENTIMENT RECOMMENDATION TEST")
print("=" * 60)
print(f"Movies available: {len(movies)}")

test_movies = ["Wonder", "Avengers: Infinity War"]

for title in test_movies:
    print(f"\nRecommendations for: {title}")
    print("-" * 60)

    selected_movie = next(
        (movie for movie in movies
         if movie["title"].lower() == title.lower()),
        None
    )

    if selected_movie is None:
        print("Movie not found.")
        continue

    original_sentiment = calculate_sentiment(
        selected_movie.get("overview", "")
    )

    print(f"Original Movie Sentiment: {original_sentiment}")

    recommendations = recommend_by_sentiment(
        title, movies, top_n=5
    )

    for index, movie in enumerate(recommendations, start=1):
        print(f"\n{index}. {movie['title']} ({movie['year']})")
        print(f"   Sentiment Score: {movie['sentiment_score']}")
        print(
            f"   Sentiment Similarity: "
            f"{movie['sentiment_similarity']:.4f}"
        )
        print(f"   Genres: {', '.join(movie['genres'])}")