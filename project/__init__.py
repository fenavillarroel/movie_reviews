from fastapi import FastAPI

from project.db import database as cnn

from project.db import User
from project.db import Movie
from project.db import UserReview

app = FastAPI()

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
