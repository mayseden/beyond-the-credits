import requests
import streamlit as st

BASE_URL = "https://api.themoviedb.org/3"


def tmdb_request(endpoint, params=None):
    """Send a request to TMDB and return the JSON response."""

    api_key = st.secrets["TMDB_API_KEY"]

    request_params = {
        "api_key": api_key,
        "language": "en-US"
    }

    if params:
        request_params.update(params)

    url = f"{BASE_URL}/{endpoint.lstrip('/')}"

    try:
        response = requests.get(
            url,
            params=request_params,
            timeout=15
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        print(f"TMDB API error: {error}")
        return None


def search_movies(query, page=1):
    """Search for movies by title."""

    return tmdb_request(
        "search/movie",
        {
            "query": query,
            "page": page,
            "include_adult": "false"
        }
    )


def get_movie_details(movie_id):
    """Retrieve detailed movie information."""

    return tmdb_request(
        f"movie/{movie_id}",
        {
            "append_to_response":
                "credits,keywords,release_dates"
        }
    )


def get_trending_movies():
    """Retrieve movies trending this week."""

    return tmdb_request("trending/movie/week")


def get_similar_movies(movie_id):
    """Retrieve movies similar to a selected movie."""

    return tmdb_request(f"movie/{movie_id}/similar")

# --------------------------------------------------
# MOVIE TRAILER RETRIEVAL
# --------------------------------------------------

def get_movie_trailer(movie_id):
    """
    Retrieve a movie trailer from TMDB.

    Prioritize official YouTube trailers.
    Return the YouTube video URL or None.
    """

    response = tmdb_request(
        f"movie/{movie_id}/videos"
    )

    if not response:
        return None

    videos = response.get("results", [])

    # Find official YouTube trailers first
    official_trailers = [
        video
        for video in videos
        if video.get("site") == "YouTube"
        and video.get("type") == "Trailer"
        and video.get("official") is True
    ]

    # Fall back to other YouTube trailers
    other_trailers = [
        video
        for video in videos
        if video.get("site") == "YouTube"
        and video.get("type") == "Trailer"
    ]

    # Fall back to YouTube teasers
    teasers = [
        video
        for video in videos
        if video.get("site") == "YouTube"
        and video.get("type") == "Teaser"
    ]

    selected_video = None

    if official_trailers:
        selected_video = official_trailers[0]

    elif other_trailers:
        selected_video = other_trailers[0]

    elif teasers:
        selected_video = teasers[0]

    if selected_video:
        video_key = selected_video.get("key")

        if video_key:
            return f"https://www.youtube.com/watch?v={video_key}"

    return None