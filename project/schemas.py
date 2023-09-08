from pydantic import BaseModel
from pydantic import field_validator

class MovieRequestModel(BaseModel):
    title: str

class MovieResponseModel(BaseModel):
    id: int
    title: str

class ReviewValidator:
    @field_validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('Score fuera de Rango 1 y 5')
        return score

class UserRequestModel(BaseModel):
    username: str
    password: str


class UserResposeModel(BaseModel):
    id: int
    username: str

class ReviewRequestModel(BaseModel, ReviewValidator):
    movie_id: int
    reviews: str
    score: int

class ReviewResponseModel(BaseModel):
    id: int
    user: UserResposeModel
    movie : MovieResponseModel
    reviews: str
    score: int

class ReviewRequestPutModel(BaseModel, ReviewValidator):
    reviews: str
    score: int



