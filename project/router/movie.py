from fastapi import APIRouter
from fastapi import Depends

from project.db import Movie
from project.db import User

from project.schemas import MovieResponseModel
from project.schemas import MovieRequestModel

from ..tools.tokens import get_current_user

movies_router = APIRouter(prefix='/movies')

@movies_router.post('', response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel,
                       user: User = Depends(get_current_user)):

    movie_db = Movie(
        title=movie.title
    )

    movie_db.save()

    return MovieResponseModel(
        id=movie_db.id,
        title=movie.title
    )