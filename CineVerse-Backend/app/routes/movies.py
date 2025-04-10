from fastapi import APIRouter, HTTPException, Query, Depends, status
from app.schemas.movie import MovieListResponse, MovieDetailResponse, ErrorResponse, MovieBase
from app.services import data_service
from app.preprocessing import load_data, preprocess_data
from app.model import train_model
from random import choice

router = APIRouter(prefix="/movies", tags=["Movies"])

movies, ratings = load_data()
movies_processed, ratings_processed = preprocess_data(movies, ratings)
model, movies_pivot, movies_sparse = train_model(
    movies_processed, ratings_processed)


@router.get("", response_model=MovieListResponse)
async def get_all_movies():
    """
    Retrieves a list of all movies.
    """
    movies = data_service.get_movies()
    print(movies)
    return MovieListResponse(data=[MovieBase(**m.__dict__) for m in movies])


@router.get("/{movie_id}", response_model=MovieDetailResponse, responses={404: {"model": ErrorResponse}})
async def get_movie_by_id(movie_id: str):
    """
    Retrieves details for a specific movie by its ID.
    """
    movie = data_service.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )
    return MovieDetailResponse(data=MovieBase(**movie.__dict__))


@router.get("/search/{query}", response_model=MovieListResponse)
async def search_movies(query: str):
    """
    Searches for movies matching the query string.
    """
    print("debug line 1.......")
    movies = data_service.search_movies(query)
    return MovieListResponse(data=[MovieBase(**m.__dict__) for m in movies])


@router.get("/genre/{genre_name}", response_model=MovieListResponse)
async def get_movies_by_genre(genre_name: str):
    """
    Retrieves movies belonging to a specific genre.
    """
    movies = data_service.get_movies_by_genre(genre_name)
    return MovieListResponse(data=[MovieBase(**m.__dict__) for m in movies])


@router.get("/mood/{mood_name}", response_model=MovieListResponse)
async def get_movies_by_mood(mood_name: str):
    """
    Retrieves movies matching a specific mood.
    """
    movies = data_service.get_movies_by_mood(mood_name)
    return MovieListResponse(data=[MovieBase(**m.__dict__) for m in movies])


@router.get("/recommended/{user_id}", response_model=MovieListResponse)
async def get_recommended_movies(user_id: str):
    """
    Retrieves recommended movies for a user, optionally filtered by mood.
    """
    user = data_service.get_user_by_id(user_id)
    if not user:
        pass

    movies = data_service.get_recommended_movies(user_id)
    return MovieListResponse(data=[MovieBase(**m.__dict__) for m in movies])


@router.get("/ai/recommendations/{movie_name}")
async def get_recommendations(movie_name: str) -> dict:
    _, suggestions_id = model.kneighbors(
        movies_pivot.loc[movie_name].values.reshape(1, -1))
    movie_list = [
        movie for movie in movies_pivot.index[suggestions_id[0]] if movie != movie_name]
    recommendation = choice(movie_list)

    return {"movie_recommendation": recommendation}
