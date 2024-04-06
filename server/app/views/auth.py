from jose import JWTError, jwt
from werkzeug.exceptions import Unauthorized
import time

JWT_ISSUER = "PizzaMeow.ru"
JWT_SECRET = "change_this"
JWT_LIFETIME_SECONDS = 2 * 60 * 60  # Токен будет истекать через два часа после получения
JWT_ALGORITHM = "HS256"


def authenticate(email: str, password: str):
    from .users import open_db
    DATA = open_db()
    USERS = DATA['USERS']
    for user_id in USERS:
        if USERS[user_id]['email'] == email and USERS[user_id]['password'] == password:
            return generate_token(user_id)
    return ''  # Вообще тут должно вызываться исключение, я думаю


def generate_token(user_id):
    timestamp = int(time.time())
    payload = {
        'iss': str(JWT_ISSUER),
        'iat': int(timestamp),
        'exp': int(timestamp + JWT_LIFETIME_SECONDS),
        'sub': str(user_id)
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise Unauthorized from e