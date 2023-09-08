from typing import List
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from project.schemas import ReviewResponseModel
from project.schemas import ReviewRequestPutModel
from project.schemas import ReviewRequestModel

from project.db import User
from project.db import Movie
from project.db import UserReview

from ..tools.tokens import oauth2_schema
from project.tools.tokens import get_current_user


reviews_router = APIRouter(prefix='/reviews')


@reviews_router.post('', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel,
                        user: User = Depends(get_current_user)):

    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        return HTTPException(status_code=404, detail='Movie not Found')

    user_review = UserReview.create(
        user_id = user.id,
        movie_id = user_review.movie_id,
        reviews = user_review.reviews,
        score = user_review.score
    )

    return user_review

@reviews_router.get('', response_model=List[ReviewResponseModel])
async def get_reviews(user: User = Depends(get_current_user),
                      page: int = 1,
                      limit: int = 10):

    user_reviews = UserReview.select().where(UserReview.user_id == user.id).paginate(page, limit)
    return [user_review for user_review in user_reviews]

@reviews_router.get('/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id: int,
                     user: User = Depends(get_current_user)):

    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review.user_id != user.id:
        raise HTTPException(status_code=401, detail='Owner Review is different')

    if user_review is None:
        raise HTTPException(status_code=404, detail='Review Not found')

    return user_review

@reviews_router.put('/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel,
                        user: User = Depends(get_current_user)):

    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail='Review Not found')

    if user_review.user_id != user.id:
        raise HTTPException(status_code=401, detail='Owner Review is different')

    user_review.reviews = review_request.reviews
    user_review.score = review_request.score

    user_review.save()

    return user_review

@reviews_router.delete('/{review_id}', response_model=ReviewResponseModel)
async def delete_review(review_id: int,
                        user: User = Depends(get_current_user)):

    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail='Review Not found')

    if user_review.user_id != user.id:
        raise HTTPException(status_code=401, detail='Owner Review is different')

    user_review.delete_instance()

    return user_review
