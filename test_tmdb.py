import requests
import streamlit as st

# Read the API key securely from Streamlit secrets
API_KEY = st.secrets["TMDB_API_KEY"]

# TMDB API endpoint for Wonder (2017)
url = "https://api.themoviedb.org/3/movie/406997"

# Send a request to TMDB
params = {
    "api_key": API_KEY,
    "language": "en-US"
}

try:
    response = requests.get(
        url,
        params=params,
        timeout=15
    )

    # Check whether the API request was successful
    response.raise_for_status()

    # Convert the JSON response into a Python dictionary
    movie = response.json()

    # Display the retrieved movie information
    print("\nBEYOND THE CREDITS - TMDB API TEST")
    print("----------------------------------")
    print("Title:", movie.get("title"))
    print("Release Date:", movie.get("release_date"))
    print("Runtime:", movie.get("runtime"), "minutes")
    print("Rating:", movie.get("vote_average"))
    print("Vote Count:", movie.get("vote_count"))
    print("Revenue:", movie.get("revenue"))
    print("Overview:", movie.get("overview"))

    print("\nSUCCESS! TMDB API connection is working.")

except requests.exceptions.RequestException as error:
    print("\nERROR: Could not retrieve movie data.")
    print(error)