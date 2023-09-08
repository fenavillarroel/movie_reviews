import jwt
from datetime import datetime
from datetime import timedelta

from ..db import User

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from fastapi import status

SECRET_KEY = 'jhdjajsdgjsghd'

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/api/v1/users/auth')

def create_token(user, minutes=60):
    data = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=minutes)
    }

    return jwt.encode(data, SECRET_KEY, algorithm='HS256')

def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None

def get_current_user(token: str = Depends(oauth2_schema)) -> User:
    data = decode_access_token(token)

    if data:
        return User.select().where(User.id == data['user_id']).first()
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid or expired Token',
        headers={
            'WWW-Authenticate': 'Bearer'
        }
    )