
from recommender import load_movies
from hybrid_recommender import recommend_hybrid

movies = load_movies()

print("\nBEYOND THE CREDITS - HYBRID RECOMMENDATION TEST")
print("=" * 60)
print(f"Movies available: {len(movies)}")

test_movies = ["Wonder", "Avengers: Infinity War"]

for title in test_movies:
    print(f"\nRecommendations for: {title}")
    print("-" * 60)

    recommendations = recommend_hybrid(
        title,
        movies,
        top_n=5
    )

    if not recommendations:
        print("No recommendations found.")
        continue

    for index, movie in enumerate(recommendations, start=1):
        print(
            f"\n{index}. {movie['title']} "
            f"({movie.get('release_year', 'Unknown')})"
        )

        print(
            f"   Content Similarity: "
            f"{movie['similarity_score']:.4f}"
        )

        print(
            f"   Sentiment Recommendation Score: "
            f"{movie['sentiment_recommendation_score']:.4f}"
        )

        print(
            f"   Hybrid Score: "
            f"{movie['hybrid_score']:.4f}"
        )

        print(
            f"   Genres: {', '.join(movie.get('genres', []))}"
        )