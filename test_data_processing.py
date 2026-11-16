
from tmdb_client import get_movie_details
from data_processing import process_movie


def test_movie_processing(movie_id):
    """Retrieve and process a movie from TMDB."""

    # Retrieve movie information
    movie_data = get_movie_details(movie_id)

    if not movie_data:
        print("ERROR: Could not retrieve movie information.")
        return

    # Process the movie information
    movie = process_movie(movie_data)

    print("\n" + "=" * 60)
    print("BEYOND THE CREDITS - DATA PROCESSING TEST")
    print("=" * 60)

    print("Title:", movie["title"])
    print("Release Year:", movie["release_year"])
    print("Runtime:", movie["runtime"])
    print("Language:", movie["language"])
    print("Certification:", movie["certification"])
    print("Genres:", movie["genres"])
    print("Cast:", movie["cast"])
    print("Directors:", movie["directors"])
    print("Keywords:", movie["keywords"][:10])
    print("Rating:", movie["rating"])

    print("\nCOMBINED TEXT FOR RECOMMENDATIONS:")
    print(movie["combined_text"][:500])

    print("\nSUCCESS: Movie data processed!")


# Test Wonder (2017)
test_movie_processing(406997)

# Test Avengers: Infinity War (2018)
test_movie_processing(299536)