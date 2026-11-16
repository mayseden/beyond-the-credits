
import re


def clean_text(text):
    """Clean text for natural language processing."""

    if not text:
        return ""

    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def process_movie(movie):
    """Convert TMDB movie details into structured data."""

    # Extract genres
    genres = [
        genre["name"]
        for genre in movie.get("genres", [])
    ]

    # Extract cast
    credits = movie.get("credits", {})

    cast = [
        actor["name"]
        for actor in credits.get("cast", [])[:5]
    ]

    # Extract directors
    directors = [
        person["name"]
        for person in credits.get("crew", [])
        if person.get("job") == "Director"
    ]

    # Extract keywords
    keyword_data = movie.get("keywords", {})

    keywords = [
        keyword["name"]
        for keyword in keyword_data.get("keywords", [])
    ]

    # Extract certification
    certification = "Not Rated"

    for country in movie.get("release_dates", {}).get("results", []):
        if country.get("iso_3166_1") == "US":
            for release in country.get("release_dates", []):
                if release.get("certification"):
                    certification = release["certification"]
                    break
            break

    # Combine important text features
    combined_text = " ".join(
        [movie.get("overview") or ""]
        + genres * 3
        + keywords * 2
        + cast
        + directors
    )

    # Return a standardized movie record
    return {
        "id": movie.get("id"),
        "title": movie.get("title"),
        "release_date": movie.get("release_date"),
        "release_year": (
            int(movie["release_date"][:4])
            if movie.get("release_date") else None
        ),
        "runtime": movie.get("runtime"),
        "language": movie.get("original_language"),
        "certification": certification,
        "genres": genres,
        "cast": cast,
        "directors": directors,
        "keywords": keywords,
        "overview": movie.get("overview") or "",
        "rating": movie.get("vote_average", 0),
        "vote_count": movie.get("vote_count", 0),
        "revenue": movie.get("revenue", 0),
        "poster_path": movie.get("poster_path"),
        "combined_text": clean_text(combined_text)
    }