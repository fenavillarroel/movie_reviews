from fastapi import HTTPException
from project import app

from project.schemas import UserRequestModel
from project.schemas import UserResposeModel
from project.db import User

@app.post('/users', response_model = UserResposeModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        return HTTPException(409, 'El username ya existe')

    hash_password = User.create_password(user.password)
    user = User.create(
        username = user.username,
        password = hash_password
    )

    return UserResposeModel(
        id=user.id,
        username=user.username
    )