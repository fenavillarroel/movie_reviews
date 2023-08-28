from typing import List
from fastapi import HTTPException
from project import app

from project.schemas import ReviewResponseModel
from project.schemas import ReviewRequestPutModel
from project.schemas import ReviewRequestModel

from project.db import User
from project.db import Movie
from project.db import UserReview


@app.post('/reviews', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):

    if User.select().where(User.id == user_review.user_id).first() is None:
        return HTTPException(status_code=404, detail='User not Found')

    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        return HTTPException(status_code=404, detail='Movie not Found')

    user_review = UserReview.create(
        user_id = user_review.user_id,
        movie_id = user_review.movie_id,
        reviews = user_review.reviews,
        score = user_review.score
    )

    return user_review

@app.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):

    reviews = UserReview.select().paginate(page, limit)

    return [review for review in reviews]

@app.get('/reviews/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id: int):

    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail='Review Not found')

    return user_review

@app.put('/reviews/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):

    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail='Review Not found')

    user_review.reviews = review_request.reviews
    user_review.score = review_request.score

    user_review.save()

    return user_review

@app.delete('/reviews/{review_id}', response_model=ReviewResponseModel)
async def delete_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail='Review Not found')

    user_review.delete_instance()

    return user_review
