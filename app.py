
import streamlit as st

from recommender import load_movies
from hybrid_recommender import recommend_hybrid
from movie_filters import filter_movies
from tmdb_client import get_movie_trailer


from recommendation_explanations import explain_recommendation
from natural_language_search import search_movies_by_description
from watchlist_recommender import recommend_from_watchlist
from tmdb_client import get_trending_movies




# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Beyond the Credits",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# LOAD MOVIE DATA
# --------------------------------------------------

@st.cache_data
def get_movie_data():
    return load_movies()


movies = get_movie_data()

@st.cache_data(ttl=3600)
def load_movie_trailer(movie_id):
    """Retrieve and cache a movie trailer from TMDB."""
    return get_movie_trailer(movie_id)

def show_trailer_link(movie_id, key):
    """Show a trailer link when TMDB has a YouTube trailer."""

    if movie_id is None:
        return

    trailer_url = load_movie_trailer(movie_id)

    if trailer_url:
        st.link_button(
            "▶ Watch Trailer on YouTube",
            trailer_url,
            type="secondary"
        )
    else:
        st.caption("🎬 Trailer currently unavailable.")



# Store saved movie IDs during the user's current session
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []


def add_to_watchlist(movie_id):
    """Save a movie without creating duplicates."""
    if movie_id not in st.session_state.watchlist:
        st.session_state.watchlist.append(movie_id)


def remove_from_watchlist(movie_id):
    """Remove a saved movie."""
    if movie_id in st.session_state.watchlist:
        st.session_state.watchlist.remove(movie_id)


# --------------------------------------------------
# CINEMATIC STYLING
# --------------------------------------------------

st.markdown("""
<style>

    .stApp {
        background-color: #110D12;
        color: #F6F0E8;
    }

    [data-testid="stSidebar"] {
        background-color: #21131D;
        border-right: 1px solid #5D3446;
        color: #F6F0E8;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #E8DCE1 !important;
    }

    h1, h2, h3 {
        color: #F1D3A0 !important;
    }

    .hero {
        padding: 45px 35px;
        border-radius: 18px;
        background: linear-gradient(
            120deg,
            #481A31 0%,
            #21131D 60%,
            #110D12 100%
        );
        border: 1px solid #78546A;
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #F1D3A0;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #E5D5D9;
    }

    .section-label {
        color: #D8B879;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    div.stButton > button[kind="primary"] {
        background-color: #8E3758;
        color: white;
        border: 1px solid #C69B67;
        border-radius: 10px;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #AD4C70;
        color: white;
    }

    /* Improve form label readability */

    [data-testid="stMain"] label,
    [data-testid="stMain"] label p,
    [data-testid="stMain"] .stWidgetLabel p {
        color: #E8DCE1 !important;
    }

    [data-testid="stMain"] [data-testid="stMarkdownContainer"] p {
        line-height: 1.7;
    }

    /* Make search input and text area readable */

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        color: #24151F !important;
        background-color: #FFFFFF !important;
        -webkit-text-fill-color: #24151F !important;
    }

    /* Make placeholder text readable */

    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder {
        color: #777078 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #777078 !important;
    }

    /* Keep text visible while typing or selecting */

    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        color: #24151F !important;
        -webkit-text-fill-color: #24151F !important;
    }

    /* Make all movie action buttons readable */

    div.stButton > button {
        background-color: #48243A !important;
        color: #FFFFFF !important;
        border: 1px solid #D8B879 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    div.stButton > button p,
    div.stButton > button span {
        color: #FFFFFF !important;
    }

    div.stButton > button:hover {
        background-color: #71354F !important;
        color: #FFFFFF !important;
        border-color: #F1D3A0 !important;
    }

    div.stButton > button:disabled {
        background-color: #382A34 !important;
        color: #D8C7D0 !important;
        border-color: #69515E !important;
        opacity: 1 !important;
    }

    div.stButton > button:disabled p {
        color: #D8C7D0 !important;
    }


</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🎬 Beyond the Credits")

    st.caption("Your next favourite story starts here.")

    st.divider()

    page = st.radio(
        "Explore",
        [
            "Discover Movies",
            "Trending Now",
            "My Watchlist",
            "Movie Insights",
            "About"
        ]
    )

    st.divider()

    st.caption(
        "Powered by TMDB • Built with Python & Streamlit"
    )


# --------------------------------------------------
# DISCOVER MOVIES PAGE
# --------------------------------------------------

if page == "Discover Movies":

    # Hero section

    
    st.markdown(
        """
<div class="hero">
    <div class="hero-title">Beyond the Credits</div>
    <div class="hero-subtitle">
        Because every great movie leaves something behind.
    </div>
    <p style="color:#CBB8C2; margin-top:18px;">
        Discover movies that match your interests,
        explore meaningful recommendations,
        and find your next unforgettable story.
    </p>
</div>
        """,
        unsafe_allow_html=True
    )

    # Movie search

   
    search_mode = st.radio(
        "How would you like to discover movies?",
        [
            "Search by Movie Title",
            "Describe What You Want to Watch"
        ],
        horizontal=True
    )

    if search_mode == "Search by Movie Title":
        search_query = st.text_input(
            "What movie do you love?",
            placeholder="Try Wonder or Avengers: Infinity War"
        )
    else:
        search_query = st.text_area(
            "Describe your ideal movie",
            placeholder=(
                "I want an emotional family drama "
                "about friendship and overcoming challenges."
            ),
            height=100
        )

    # --------------------------------------------------
    # MOVIE FILTER CONTROLS
    # --------------------------------------------------

    with st.expander("🎛️ Customize Your Recommendations"):

        # Release period

        st.markdown("#### Release Period")

        decade = st.selectbox(
            "Choose a Decade",
            [
                "Any Decade",
                "1950s",
                "1960s",
                "1970s",
                "1980s",
                "1990s",
                "2000s",
                "2010s",
                "2020s"
            ]
        )
        year_col1, year_col2 = st.columns(2)

        with year_col1:

            year_min = st.number_input(
                "From Year",
                min_value=1900,
                max_value=2100,
                value=1900
            )

        with year_col2:

            year_max = st.number_input(
                "To Year",
                min_value=1900,
                max_value=2100,
                value=2100
            )

        # Quality filters

        st.markdown("#### Movie Quality")

        rating_col, votes_col = st.columns(2)

        with rating_col:

            min_rating = st.slider(
                "Minimum TMDB Rating",
                min_value=0.0,
                max_value=10.0,
                value=0.0,
                step=0.5
            )

        with votes_col:

            min_votes = st.number_input(
                "Minimum Vote Count",
                min_value=0,
                value=0,
                step=100
            )

        # Content filters

        st.markdown("#### Content Preferences")

        runtime_col1, runtime_col2 = st.columns(2)

        with runtime_col1:

            runtime_min = st.number_input(
                "Minimum Runtime (minutes)",
                min_value=0,
                value=0
            )

        with runtime_col2:

            runtime_max = st.number_input(
                "Maximum Runtime (minutes)",
                min_value=0,
                value=300
            )

        certification = st.selectbox(
            "Certification",
            ["Any", "G", "PG", "PG-13", "R", "NC-17"]
        )

        language = st.selectbox(
            "Original Language",
            ["Any", "en", "fr", "es", "ko", "ja", "hi"]
        )

        # Personnel filters

        st.markdown("#### Cast and Crew")

        actor = st.text_input(
            "Preferred Actor",
            placeholder="e.g. Tom Hanks"
        )

        director = st.text_input(
            "Preferred Director",
            placeholder="e.g. Christopher Nolan"
        )

        # Genre filters

        st.markdown("#### Genre Preferences")

        available_genres = sorted({
            genre
            for movie in movies
            for genre in movie.get("genres", [])
        })

        selected_genres = st.multiselect(
            "Select Genres",
            available_genres
        )

        genre_logic = st.radio(
            "Genre Matching",
            ["OR", "AND"],
            horizontal=True
        )

    
    # --------------------------------------------------
    # RECOMMENDATION BUTTON
    # --------------------------------------------------

    
    if "show_recommendations" not in st.session_state:
        st.session_state.show_recommendations = False

    if st.button("Find My Next Movie", type="primary"):
        st.session_state.show_recommendations = True

    if st.session_state.show_recommendations:

        query = search_query.strip()

        if not query:
            st.warning("Please enter a movie title or description.")

        elif year_min > year_max:
            st.warning(
                "The starting year cannot be greater "
                "than the ending year."
            )

        elif runtime_min > runtime_max:
            st.warning(
                "Minimum runtime cannot be greater "
                "than maximum runtime."
            )

        else:

            selected_movie = None

            if search_mode == "Search by Movie Title":

                selected_movie = next(
                    (
                        movie for movie in movies
                        if movie["title"].lower() == query.lower()
                    ),
                    None
                )

                if selected_movie is None:
                    st.warning(
                        "Movie not found in our collection. "
                        "Please check the title and try again."
                    )

            if (
                search_mode == "Describe What You Want to Watch"
                or selected_movie is not None
            ):

                with st.spinner(
                    "Finding your next favourite movie..."
                ):

                    if search_mode == "Search by Movie Title":

                        recommendations = recommend_hybrid(
                            query,
                            movies,
                            top_n=len(movies)
                        )

                    else:

                        recommendations = (
                            search_movies_by_description(
                                query,
                                movies,
                                top_n=len(movies)
                            )
                        )

                    # Combine decade and year preferences
                    effective_year_min = year_min
                    effective_year_max = year_max

                    if decade != "Any Decade":
                        decade_start = int(decade[:4])
                        effective_year_min = max(
                            year_min, decade_start
                        )
                        effective_year_max = min(
                            year_max, decade_start + 9
                        )

                    # Apply all required filters
                    recommendations = filter_movies(
                        recommendations,
                        year_min=effective_year_min,
                        year_max=effective_year_max,
                        min_rating=min_rating,
                        min_votes=min_votes,
                        runtime_min=runtime_min,
                        runtime_max=runtime_max,
                        certification=(
                            None if certification == "Any"
                            else certification
                        ),
                        language=(
                            None if language == "Any"
                            else language
                        ),
                        actor=actor.strip() or None,
                        director=director.strip() or None,
                        genres=selected_genres or None,
                        genre_logic=genre_logic
                    )

                    recommendations = recommendations[:5]

                if not recommendations:

                    st.info(
                        "No movies match your search and filters. "
                        "Try a different description or adjust "
                        "your preferences."
                    )

                else:

                    st.success(
                        f"Found {len(recommendations)} "
                        "movie recommendations!"
                    )

                # Show the exact searched movie before recommendations
                if search_query.strip():

                    selected_movie = next(
                        (
                            movie for movie in movies
                            if movie.get("title", "").casefold()
                            == search_query.strip().casefold()
                        ),
                        None
                    )

                    if selected_movie:

                        st.subheader("🎬 Your Selected Movie")

                        with st.container(border=True):

                            poster_col, details_col = st.columns(
                                [1, 3],
                                gap="medium"
                            )

                            with poster_col:

                                poster_path = selected_movie.get(
                                    "poster_path"
                                )

                                if poster_path:
                                    st.image(
                                        "https://image.tmdb.org/t/p/w342"
                                        + poster_path,
                                        width="stretch"
                                    )
                                else:
                                    st.info("Poster unavailable")

                            with details_col:

                                st.markdown(
                                    f"### {selected_movie['title']} "
                                    f"({selected_movie.get('release_year', 'Unknown')})"
                                )

                                rating = selected_movie.get("rating")
                                votes = selected_movie.get("vote_count")

                                if rating is not None:
                                    st.write(
                                        f"⭐ TMDB Rating: {rating:.1f}/10"
                                    )

                                if votes is not None:
                                    st.write(
                                        f"👥 {votes:,} votes"
                                    )

                                genres = selected_movie.get("genres") or []

                                st.write(
                                    "**Genres:** "
                                    + (
                                        ", ".join(genres)
                                        if genres else "Unknown"
                                    )
                                )

                                st.write(
                                    selected_movie.get("overview")
                                    or "No plot summary available."
                                )

                                
                                # Selected movie actions
                                movie_id = selected_movie.get("id")

                                if movie_id is not None:

                                    # Save to Watchlist
                                    if movie_id in st.session_state.watchlist:
                                        st.button(
                                            "✓ Saved to Watchlist",
                                            key=f"selected_saved_{movie_id}",
                                            disabled=True
                                        )

                                    else:
                                        st.button(
                                            "♡ Save to Watchlist",
                                            key=f"selected_save_{movie_id}",
                                            on_click=add_to_watchlist,
                                            args=(movie_id,)
                                        )

                                    # Watch Trailer for selected movie
                                    show_trailer_link(
                                        movie_id,
                                        key=f"selected_trailer_{movie_id}"
                                    )


                        st.divider()

                    st.subheader("Recommended For You")

                    for movie in recommendations:

                        with st.container(border=True):

                            poster_path = movie.get("poster_path")

                            poster_url = (
                                "https://image.tmdb.org/t/p/w342"
                                + poster_path
                                if poster_path else None
                            )

                            poster_col, details_col = st.columns(
                                [1, 3],
                                gap="medium"
                            )

                            with poster_col:
                                if poster_url:
                                    st.image(
                                        poster_url,
                                        width="stretch"
                                    )
                                else:
                                    st.info("🎬 Poster unavailable")

                            with details_col:

                                title = movie.get(
                                    "title", "Untitled"
                                )
                                year = movie.get(
                                    "release_year", "Unknown"
                                )

                                st.markdown(
                                    f"### {title} ({year})"
                                )

                                rating = movie.get("rating")
                                votes = movie.get("vote_count")

                                if rating is not None and rating > 0:
                                    st.write(
                                        f"⭐ TMDB Rating: "
                                        f"{rating:.1f}/10"
                                    )
                                else:
                                    st.write(
                                        "⭐ TMDB Rating: Not yet rated"
                                    )

                                if votes is not None and votes > 0:
                                    st.write(
                                        f"👥 {votes:,} votes"
                                    )
                                else:
                                    st.write(
                                        "👥 No votes available"
                                    )

                                genres = movie.get("genres") or []

                                st.write(
                                    "**Genres:** "
                                    + (
                                        ", ".join(genres)
                                        if genres else "Unknown"
                                    )
                                )

                                st.write(
                                    movie.get("overview")
                                    or "No plot summary available."
                                )

                                # Save or remove a movie from the watchlist
                                movie_id = movie.get("id")

                                if movie_id is not None:

                                    if movie_id in st.session_state.watchlist:

                                        st.button(
                                            "✓ Saved to Watchlist",
                                            key=f"saved_{movie_id}",
                                            disabled=True
                                        )

                                    else:

                                        st.button(
                                            "♡ Save to Watchlist",
                                            key=f"save_{movie_id}",
                                            on_click=add_to_watchlist,
                                            args=(movie_id,)
                                        )

                                
                                
                                # Trailer for recommended movies
                                if movie_id is not None:
                                    show_trailer_link(
                                        movie_id,
                                        key=f"recommended_trailer_{movie_id}"
                                    )


                                if search_mode == "Search by Movie Title":

                                    st.caption(
                                        "Hybrid match score: "
                                        f"{movie.get('hybrid_score', 0):.2f}"
                                    )

                                    explanations = explain_recommendation(
                                        selected_movie,
                                        movie
                                    )

                                    with st.expander("💡 Why This Movie?"):
                                        for explanation in explanations:
                                            st.write(f"• {explanation}")

                                else:

                                    st.caption(
                                        "Description match score: "
                                        f"{movie.get('query_similarity_score', 0):.2f}"
                                    )

                                    st.caption(
                                        "Matched using NLP analysis of "
                                        "movie plots, genres, and keywords."
                                    )

    # Discover page footer

    st.divider()

    st.subheader(
        "Discover something extraordinary"
    )

    st.write(
        "Explore personalized movie recommendations "
        "powered by content analysis and sentiment matching."
    )


# --------------------------------------------------
# TRENDING PAGE
# --------------------------------------------------

elif page == "Trending Now":

    st.title("🔥 Trending Now")

    st.write(
        "Discover movies audiences are talking about "
        "and explore what's trending this week."
    )

    @st.cache_data(ttl=3600)
    def load_trending_movies():
        response = get_trending_movies()

        if response and "results" in response:
            return response["results"]

        return []

    with st.spinner("Loading trending movies..."):
        trending_movies = load_trending_movies()

    if not trending_movies:
        st.warning(
            "Trending movies are temporarily unavailable. "
            "Please try again later."
        )

    else:
        st.success(
            f"Showing {len(trending_movies)} trending movies this week!"
        )

        for movie in trending_movies:

            with st.container(border=True):

                poster_col, details_col = st.columns(
                    [1, 3],
                    gap="medium"
                )

                with poster_col:

                    poster_path = movie.get("poster_path")

                    if poster_path:
                        poster_url = (
                            "https://image.tmdb.org/t/p/w342"
                            + poster_path
                        )

                        st.image(poster_url, width="stretch")

                    else:
                        st.info("🎬 Poster unavailable")

                with details_col:

                    title = movie.get("title", "Unknown Movie")

                    release_date = movie.get(
                        "release_date", ""
                    )

                    release_year = (
                        release_date[:4]
                        if release_date
                        else "Unknown"
                    )

                    st.markdown(
                        f"### {title} ({release_year})"
                    )

                    rating = movie.get(
                        "vote_average", 0
                    )

                    votes = movie.get(
                        "vote_count", 0
                    )

                    st.write(
                        f"⭐ TMDB Rating: {rating:.1f}/10"
                    )

                    st.write(
                        f"👥 {votes:,} votes"
                    )

                    st.write(
                        movie.get("overview")
                        or "No plot summary available."
                    )


# --------------------------------------------------
# WATCHLIST PAGE
# --------------------------------------------------


elif page == "My Watchlist":

    st.title("❤️ My Watchlist")
    st.write(
        "Your personal movie collection, "
        "with recommendations based on your interests."
    )

    # Find movies saved during the current session
    saved_movies = [
        movie
        for movie in movies
        if movie.get("id") in st.session_state.watchlist
    ]

    if not saved_movies:
        st.info(
            "Your watchlist is currently empty. "
            "Go to Discover Movies and save a movie "
            "to start building your collection."
        )

    else:
        st.success(
            f"You have {len(saved_movies)} "
            f"movie(s) in your watchlist!"
        )

        st.subheader("Your Saved Movies")

        for movie in saved_movies:

            with st.container(border=True):

                poster_col, details_col = st.columns(
                    [1, 3],
                    gap="medium"
                )

                with poster_col:

                    poster_path = movie.get("poster_path")

                    if poster_path:
                        st.image(
                            "https://image.tmdb.org/t/p/w342"
                            + poster_path,
                            width="stretch"
                        )
                    else:
                        st.info("Poster unavailable")

                with details_col:

                    st.markdown(
                        f"### {movie.get('title', 'Unknown')} "
                        f"({movie.get('release_year', 'Unknown')})"
                    )

                    st.write(
                        "**Genres:** "
                        + ", ".join(movie.get("genres") or [])
                    )

                    st.write(
                        movie.get("overview")
                        or "No description available."
                    )

                    st.button(
                        "Remove from Watchlist",
                        key=f"remove_{movie['id']}",
                        on_click=remove_from_watchlist,
                        args=(movie["id"],)
                    )

        st.divider()

        st.subheader("✨ Recommended Based on Your Watchlist")

        st.write(
            "These suggestions are based on the movies "
            "you have saved and their content similarities."
        )

        profile_recommendations = recommend_from_watchlist(
            st.session_state.watchlist,
            movies,
            top_n=5
        )

        if not profile_recommendations:
            st.info(
                "We couldn't find additional recommendations "
                "for your current watchlist."
            )

        else:

            for movie in profile_recommendations:

                with st.container(border=True):

                    poster_col, details_col = st.columns(
                        [1, 3],
                        gap="medium"
                    )

                    with poster_col:

                        poster_path = movie.get("poster_path")

                        if poster_path:
                            st.image(
                                "https://image.tmdb.org/t/p/w342"
                                + poster_path,
                                width="stretch"
                            )

                    
                    with details_col:

                        st.markdown(
                            f"### {movie.get('title', 'Unknown')} "
                            f"({movie.get('release_year', 'Unknown')})"
                        )

                        st.write(
                            "**Genres:** "
                            + ", ".join(movie.get("genres") or [])
                        )

                        st.write(
                            movie.get("overview")
                            or "No description available."
                        )

                        st.caption(
                            "Profile similarity score: "
                            f"{movie['profile_similarity_score']:.2f}"
                        )

                        shared_genres = movie.get(
                            "shared_profile_genres", []
                        )

                        if shared_genres:
                            st.write(
                                "**Matches your interests in:** "
                                + ", ".join(shared_genres)
                            )

                        movie_id = movie.get("id")

                        if movie_id is not None:

                            if movie_id not in st.session_state.watchlist:
                                st.button(
                                    "♡ Save to Watchlist",
                                    key=f"profile_save_{movie_id}",
                                    on_click=add_to_watchlist,
                                    args=(movie_id,)
                                )

                            # Trailer for watchlist recommendations
                            show_trailer_link(
                                movie_id,
                                key=f"profile_trailer_{movie_id}"
                            )




# --------------------------------------------------
# MOVIE INSIGHTS PAGE
# --------------------------------------------------

elif page == "Movie Insights":

    st.title("📊 Movie Insights")

    st.write(
        "Explore movie trends, ratings, genres, "
        "and interesting patterns in our movie collection."
    )

    import pandas as pd
    from collections import Counter

    # Prepare the dataset
    df = pd.DataFrame(movies)

    # Collection overview
    st.subheader("🎬 Collection Overview")

    total_movies = len(df)

    ratings = pd.to_numeric(
        df["rating"], errors="coerce"
    )

    runtimes = pd.to_numeric(
        df["runtime"], errors="coerce"
    )

    average_rating = ratings.mean()
    average_runtime = runtimes.mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Movies", total_movies)

    with col2:
        st.metric(
            "Average TMDB Rating",
            f"{average_rating:.1f}/10"
        )

    with col3:
        st.metric(
            "Average Runtime",
            f"{average_runtime:.0f} min"
        )

    st.divider()

    

    # --------------------------------------------------
    # MOST POPULAR GENRES
    # --------------------------------------------------

    from collections import Counter

    st.subheader("🎭 Most Popular Genres")

    st.write(
        "Explore the most common movie genres in our collection. "
        "A movie can belong to multiple genres, so it may be "
        "counted in more than one category."
    )

    genre_counts = Counter(
        genre
        for movie in movies
        for genre in movie.get("genres", [])
    )

    top_genres = genre_counts.most_common(10)

    genre_df = pd.DataFrame(
        top_genres,
        columns=["Movie Genre", "Number of Movies"]
    )

    st.bar_chart(
        genre_df.set_index("Movie Genre"),
        y="Number of Movies",
        color="#D8B879",
        horizontal=True
    )

    st.caption(
        "Each bar represents a movie genre. "
        "Longer bars indicate more movies in that genre. "
        "These counts describe our collection, not "
        "the popularity of genres across all TMDB movies."
    )

    # Interactive genre exploration
    with st.expander("🎬 Explore Movies by Genre"):

        selected_genre = st.selectbox(
            "Choose a movie genre",
            sorted(genre_counts.keys()),
            key="insights_genre"
        )

        matching_movies = [
            movie
            for movie in movies
            if selected_genre in movie.get("genres", [])
        ]

        st.write(
            f"**{len(matching_movies)} movies** "
            f"in our collection belong to the "
            f"**{selected_genre}** genre."
        )

        genre_movie_df = pd.DataFrame([
            {
                "Movie Title": movie.get("title", "Unknown"),
                "Release Year": movie.get(
                    "release_year", "Unknown"
                ),
                "TMDB Rating (/10)": movie.get("rating", 0),
                "Genres": ", ".join(
                    movie.get("genres", [])
                )
            }
            for movie in matching_movies
        ])

        if not genre_movie_df.empty:

            genre_movie_df = genre_movie_df.sort_values(
                by="TMDB Rating (/10)",
                ascending=False
            )

            st.dataframe(
                genre_movie_df,
                hide_index=True,
                use_container_width=True
            )

        else:
            st.info("No movies found for this genre.")

    st.divider()



    
    # Ratings distribution
    st.subheader("⭐ TMDB Ratings Distribution")

    st.write(
        "TMDB users rate movies on a scale from 0 to 10. "
        "The chart below shows how many movies in our "
        "collection fall into each rating range."
    )

    # Convert ratings into numeric values
    valid_ratings = pd.to_numeric(
        df["rating"],
        errors="coerce"
    ).dropna()

    # Group ratings into clearly labelled ranges
    rating_ranges = pd.cut(
        valid_ratings,
        bins=[-0.01, 2, 4, 6, 8, 10],
        labels=[
            "0–2",
            "2–4",
            "4–6",
            "6–8",
            "8–10"
        ],
        include_lowest=True
    )

    rating_counts = (
        rating_ranges.value_counts()
        .sort_index()
    )

    rating_chart = pd.DataFrame({
        "TMDB Rating Range": rating_counts.index.astype(str),
        "Number of Movies": rating_counts.values
    })

    st.bar_chart(
        rating_chart.set_index("TMDB Rating Range"),
        y="Number of Movies",
        color="#D8B879"
    )

    st.caption(
        "Horizontal axis: TMDB rating ranges out of 10. "
        "Vertical axis: Number of movies in each range. "
        "For example, 8–10 means movies rated above 8 "
        "and up to 10."
    )

    # Show actual movie titles behind the chart
    with st.expander("🎬 Explore Movies by Rating"):

        selected_rating = st.selectbox(
            "Choose a TMDB rating range",
            ["0–2", "2–4", "4–6", "6–8", "8–10"]
        )

        lower, upper = map(
            int,
            selected_rating.split("–")
        )

        rating_values = pd.to_numeric(
            df["rating"],
            errors="coerce"
        )

        if lower == 0:
            rating_mask = (
                (rating_values >= lower) &
                (rating_values <= upper)
            )
        else:
            rating_mask = (
                (rating_values > lower) &
                (rating_values <= upper)
            )

        matching_movies = df.loc[
            rating_mask,
            ["title", "release_year", "rating"]
        ].copy()

        matching_movies = matching_movies.sort_values(
            by="rating",
            ascending=False
        )

        matching_movies = matching_movies.rename(
            columns={
                "title": "Movie Title",
                "release_year": "Release Year",
                "rating": "TMDB Rating (/10)"
            }
        )

        st.write(
            f"**{len(matching_movies)} movies** "
            f"have ratings in the {selected_rating} range."
        )

        st.dataframe(
            matching_movies,
            hide_index=True,
            use_container_width=True
        )

    st.divider()

    
    # --------------------------------------------------
    # MOVIES BY RELEASE DECADE
    # --------------------------------------------------

    st.subheader("📅 Movies by Release Decade")

    st.write(
        "Explore how movies in our collection are distributed "
        "across different decades. Select a decade to discover "
        "the movies released during that period."
    )

    # Prepare release year data
    decade_movies = df.copy()

    decade_movies["release_year"] = pd.to_numeric(
        decade_movies["release_year"],
        errors="coerce"
    )

    decade_movies = decade_movies.dropna(
        subset=["release_year"]
    ).copy()

    decade_movies["release_year"] = (
        decade_movies["release_year"].astype(int)
    )

    # Calculate release decades
    decade_movies["Decade"] = (
        (decade_movies["release_year"] // 10) * 10
    )

    decade_counts = (
        decade_movies["Decade"]
        .value_counts()
        .sort_index()
    )

    decade_df = pd.DataFrame({
        "Release Decade": [
            f"{decade}s"
            for decade in decade_counts.index
        ],
        "Number of Movies": decade_counts.values
    })

    # Display chart
    st.bar_chart(
        decade_df.set_index("Release Decade"),
        y="Number of Movies",
        color="#D8B879"
    )

    st.caption(
        "Horizontal axis: Release decades (for example, "
        "2010s represents 2010–2019). "
        "Vertical axis: Number of movies in our collection. "
        "Upcoming movies may also be included."
    )

    # Interactive decade exploration
    with st.expander("🎬 Explore Movies by Decade"):

        available_decades = sorted(
            decade_movies["Decade"].unique(),
            reverse=True
        )

        selected_decade = st.selectbox(
            "Choose a release decade",
            available_decades,
            format_func=lambda decade: f"{decade}s",
            key="insights_decade"
        )

        matching_decade_movies = decade_movies[
            decade_movies["Decade"] == selected_decade
        ].copy()

        st.write(
            f"**{len(matching_decade_movies)} movies** "
            f"in our collection have release years between "
            f"**{selected_decade} and {selected_decade + 9}**."
        )

        display_columns = [
            "title",
            "release_year",
            "rating"
        ]

        decade_table = matching_decade_movies[
            display_columns
        ].copy()

        decade_table = decade_table.rename(
            columns={
                "title": "Movie Title",
                "release_year": "Release Year",
                "rating": "TMDB Rating (/10)"
            }
        )

        decade_table = decade_table.sort_values(
            by=["Release Year", "Movie Title"],
            ascending=[False, True]
        )

        st.dataframe(
            decade_table,
            hide_index=True,
            use_container_width=True
        )

    st.divider()



# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

elif page == "About":

    st.title("🎬 About Beyond the Credits")

    st.markdown(
        "### Because every great movie leaves something behind."
    )

    st.write(
        "Beyond the Credits is an interactive movie discovery "
        "and recommendation application designed to help "
        "people find movies that match their interests, "
        "preferences, and favourite stories."
    )

    st.write(
        "Rather than relying only on popularity or ratings, "
        "the application combines movie content analysis "
        "with sentiment-based matching to recommend films "
        "that share meaningful characteristics."
    )

    st.divider()

    # --------------------------------------------------
    # PROJECT PURPOSE
    # --------------------------------------------------

    st.subheader("🎯 Our Purpose")

    st.write(
        "Finding something to watch can be overwhelming, "
        "especially when there are thousands of movies "
        "available. Beyond the Credits aims to make movie "
        "discovery easier, more personalized, and more "
        "informative."
    )

    st.write(
        "Users can search for movies they already enjoy, "
        "describe the kinds of stories they want to watch, "
        "apply detailed filters, and explore recommendations "
        "with explanations of why each movie was suggested."
    )

    st.divider()

    # --------------------------------------------------
    # RECOMMENDATION METHODS
    # --------------------------------------------------

    st.subheader("🧠 How Our Recommendations Work")

    st.write(
        "Beyond the Credits uses two recommendation methods "
        "and combines them into a hybrid recommendation system."
    )

    with st.expander("1️⃣ Content-Based Recommendations"):

        st.write(
            "Our content-based recommendation system analyzes "
            "movie descriptions and other descriptive features "
            "to identify similarities between films."
        )

        st.write(
            "It uses TF-IDF (Term Frequency–Inverse Document "
            "Frequency) to represent movie information "
            "numerically and cosine similarity to measure "
            "how closely two movies are related."
        )

        st.write(
            "Movies with similar descriptive content receive "
            "higher content similarity scores."
        )

    with st.expander("2️⃣ Sentiment-Based Recommendations"):

        st.write(
            "Our sentiment-based recommendation system uses "
            "VADER sentiment analysis to examine the language "
            "used in movie plot summaries."
        )

        st.write(
            "It compares the sentiment scores of movie "
            "descriptions and considers shared genres "
            "when ranking recommendations."
        )

        st.write(
            "These scores reflect the sentiment expressed "
            "in plot descriptions, not audience reviews "
            "or guaranteed emotional experiences."
        )

    with st.expander("3️⃣ Hybrid Recommendation System"):

        st.write(
            "The hybrid system combines both methods "
            "to produce a final recommendation ranking."
        )

        st.markdown(
            "**Hybrid Score = "
            "70% Content Similarity + "
            "30% Sentiment-Based Recommendation Score**"
        )

        st.write(
            "This approach considers both descriptive "
            "similarity and sentiment-related characteristics."
        )

        st.caption(
            "Hybrid scores are ranking values, not "
            "probabilities or predictions of user satisfaction."
        )

    st.divider()

    # --------------------------------------------------
    # FEATURES
    # --------------------------------------------------

    st.subheader("✨ Explore Our Features")

    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:

        st.markdown("#### 🔎 Movie Discovery")
        st.write(
            "Search for movies by title and explore "
            "recommendations based on their characteristics."
        )

        st.markdown("#### 💬 Natural-Language Search")
        st.write(
            "Describe the kind of movie you want "
            "to watch using everyday language."
        )

        st.markdown("#### ❤️ Personal Watchlist")
        st.write(
            "Save movies to your watchlist and receive "
            "additional suggestions based on your saved titles."
        )

    with feature_col2:

        st.markdown("#### 🎛️ Advanced Filters")
        st.write(
            "Refine results by release year, ratings, "
            "vote count, runtime, certification, language, "
            "cast, director, and genre."
        )

        st.markdown("#### 💡 Explainable Recommendations")
        st.write(
            "Explore the reasons behind movie suggestions "
            "using available similarity information."
        )

        st.markdown("#### 📊 Movie Insights")
        st.write(
            "Explore interactive charts and tables "
            "showing movie genres, ratings, "
            "and release decades."
        )

    st.divider()

    # --------------------------------------------------
    # DATA SOURCE
    # --------------------------------------------------

    st.subheader("🎞️ Our Movie Data")

    st.write(
        "Movie information is sourced from "
        "The Movie Database (TMDB), which provides "
        "movie titles, descriptions, genres, "
        "release information, ratings, and other metadata."
    )

    st.metric(
        "Movies in Our Collection",
        f"{len(movies):,}"
    )

    st.caption(
        "Our recommendation and insights features use "
        "a curated movie collection. Results are limited "
        "to the movies included in that collection."
    )

    st.markdown(
        "[Visit The Movie Database](https://www.themoviedb.org/)"
    )

    st.caption(
        "This product uses the TMDB API but is not "
        "endorsed or certified by TMDB."
    )

    st.divider()

    # --------------------------------------------------
    # TECHNOLOGY
    # --------------------------------------------------

    st.subheader("💻 Technologies Behind the Application")

    st.markdown(
        """
        - **Python:** Core application and recommendation logic
        - **Streamlit:** Interactive web application
        - **TMDB API:** Movie information and trending data
        - **Scikit-learn:** TF-IDF and cosine similarity
        - **VADER Sentiment:** Plot-description sentiment analysis
        - **Pandas:** Data processing and analysis
        - **GitHub:** Source code and version control
        """
    )

    st.divider()

    # --------------------------------------------------
    # PROJECT CLOSING
    # --------------------------------------------------

    st.subheader("🍿 Your Next Great Movie Awaits")

    st.write(
        "Whether you're looking for something familiar, "
        "discovering a new genre, or searching for a story "
        "that matches your mood, Beyond the Credits "
        "helps you explore movies beyond their titles."
    )

    st.markdown(
        "**Beyond the Credits — "
        "Because every great movie leaves something behind.**"
    )