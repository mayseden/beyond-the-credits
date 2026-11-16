
from tmdb_client import search_movies, get_movie_details


def display_movie_information(movie_title, release_year):
    print("\n" + "=" * 55)
    print(f"SEARCHING FOR: {movie_title} ({release_year})")
    print("=" * 55)

    # Search TMDB for the movie
    search_results = search_movies(movie_title)

    if not search_results:
        print("ERROR: Could not search TMDB.")
        return

    # Find the correct movie using its title and release year
    matching_movies = [
        movie for movie in search_results.get("results", [])
        if movie.get("title", "").lower() == movie_title.lower()
        and movie.get("release_date", "").startswith(str(release_year))
    ]

    if not matching_movies:
        print("Movie not found.")
        return

    movie_id = matching_movies[0]["id"]

    # Retrieve detailed movie information
    movie = get_movie_details(movie_id)

    if not movie:
        print("ERROR: Could not retrieve movie details.")
        return

    # Extract genres
    genres = [
        genre["name"]
        for genre in movie.get("genres", [])
    ]

    # Extract top 5 cast members
    cast = [
        actor["name"]
        for actor in movie.get("credits", {}).get("cast", [])[:5]
    ]

    # Extract directors
    directors = [
        person["name"]
        for person in movie.get("credits", {}).get("crew", [])
        if person.get("job") == "Director"
    ]

    # Extract keywords
    keyword_data = movie.get("keywords", {})
    keywords = [
        keyword["name"]
        for keyword in keyword_data.get("keywords", [])
    ]

    # Extract US certification when available
    certification = "Not available"

    release_data = movie.get("release_dates", {}).get("results", [])

    for country in release_data:
        if country.get("iso_3166_1") == "US":
            for release in country.get("release_dates", []):
                if release.get("certification"):
                    certification = release["certification"]
                    break
            break

    # Display results
    print("\nMOVIE INFORMATION")
    print("-" * 55)
    print("Title:", movie.get("title"))
    print("Release Date:", movie.get("release_date"))
    print("Runtime:", movie.get("runtime"), "minutes")
    print("Original Language:", movie.get("original_language"))
    print("Certification (US):", certification)
    print("Genres:", ", ".join(genres))
    print("Rating:", movie.get("vote_average"))
    print("Vote Count:", movie.get("vote_count"))
    print("Revenue:", movie.get("revenue"))
    print("Director(s):", ", ".join(directors))
    print("Top Cast:", ", ".join(cast))
    print("Keywords:", ", ".join(keywords[:10]))
    print("Overview:", movie.get("overview"))

    print("\nSUCCESS: Movie metadata retrieved!")


# Test both movies
display_movie_information("Wonder", 2017)
display_movie_information("Avengers: Infinity War", 2018)