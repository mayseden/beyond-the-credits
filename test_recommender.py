
from recommender import load_movies, recommend_by_content


movies = load_movies()

print("\nBEYOND THE CREDITS - CONTENT RECOMMENDATION TEST")
print("=" * 60)

print(f"Movies available: {len(movies)}")

for selected_movie in ["Wonder", "Avengers: Infinity War"]:

    print(f"\nRecommendations for: {selected_movie}")
    print("-" * 60)

    recommendations = recommend_by_content(
        selected_movie,
        movies,
        top_n=5
    )

    if not recommendations:
        print("No recommendations found.")
        continue

    for index, movie in enumerate(recommendations, start=1):
        print(
            f"{index}. {movie['title']} "
            f"({movie['release_year']})"
        )

        print(
            f"   Similarity Score: "
            f"{movie['similarity_score']:.4f}"
        )

        print(
            f"   Genres: {', '.join(movie['genres'])}"
        )