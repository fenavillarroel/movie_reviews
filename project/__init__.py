from fastapi import FastAPI
from fastapi import APIRouter
from project.db import database as cnn

from .router.movie import movies_router
from .router.reviews import reviews_router
from .router.users import users_router

from project.db import User
from project.db import Movie
from project.db import UserReview

app = FastAPI(title='Movies Reviews',
              description='Reviews movies app example',
              version='1.0.0')
api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(movies_router)
api_v1.include_router(reviews_router)
api_v1.include_router(users_router)

app.include_router(api_v1)

@app.on_event('startup')
def startup():
    if cnn.is_closed():
        cnn.connect()

    cnn.create_tables([User, Movie, UserReview])

@app.on_event('shutdown')
def shotdown():
    if not cnn.is_closed():
        cnn.close()
        print('Disconnected....')
