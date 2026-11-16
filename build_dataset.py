
import json
import time
from pathlib import Path

from tmdb_client import tmdb_request, get_movie_details
from data_processing import process_movie


DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "movies.json"

# Number of pages to retrieve from each category
PAGES_PER_CATEGORY = 3

CATEGORIES = [
    "movie/popular",
    "movie/top_rated",
    "movie/now_playing"
]


def collect_movie_ids():
    """Collect unique movie IDs from TMDB."""

    movie_ids = set()

    for category in CATEGORIES:
        print(f"\nCollecting movies from {category}...")

        for page in range(1, PAGES_PER_CATEGORY + 1):
            response = tmdb_request(
                category,
                {"page": page}
            )

            if not response:
                print(f"Could not retrieve page {page}.")
                continue

            for movie in response.get("results", []):
                if movie.get("id"):
                    movie_ids.add(movie["id"])

    # Include our two demonstration movies
    movie_ids.add(406997)  # Wonder
    movie_ids.add(299536)  # Avengers: Infinity War

    return sorted(movie_ids)


def build_dataset():
    """Retrieve, process, and save movie information."""

    DATA_DIR.mkdir(exist_ok=True)

    movie_ids = collect_movie_ids()

    print(f"\nFound {len(movie_ids)} unique movies.")
    print("Retrieving detailed movie information...\n")

    movies = []

    for index, movie_id in enumerate(movie_ids, start=1):
        print(
            f"Processing movie {index}/{len(movie_ids)}",
            end=" "
        )

        movie_data = get_movie_details(movie_id)

        if not movie_data:
            print("- skipped")
            continue

        processed_movie = process_movie(movie_data)

        # Keep movies with useful information
        if (
            processed_movie["title"]
            and processed_movie["combined_text"]
        ):
            movies.append(processed_movie)
            print(f"- {processed_movie['title']}")
        else:
            print("- insufficient information")

        # Small delay to avoid sending requests too quickly
        time.sleep(0.15)

    # Save the processed dataset
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            movies,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("\n" + "=" * 55)
    print("BEYOND THE CREDITS - DATASET SUMMARY")
    print("=" * 55)

    print("Total movies saved:", len(movies))
    print("Dataset location:", DATA_FILE)

    print("\nSUCCESS: Movie dataset created!")


if __name__ == "__main__":
    build_dataset()