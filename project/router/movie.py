from project import app
from project.db import Movie

from project.schemas import MovieResponseModel
from project.schemas import MovieRequestModel

@app.post('/movies', response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):

    movie_db = Movie(
        title=movie.title
    )

    movie_db.save()

    return MovieResponseModel(
        id=movie_db.id,
        title=movie.title
    )