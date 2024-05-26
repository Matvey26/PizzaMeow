from jose import JWTError, jwt
from werkzeug.exceptions import Unauthorized
import time

JWT_ISSUER = "PizzaMeow.ru"
JWT_SECRET = "change_this"
JWT_ALGORITHM = "HS256"


def generate_token(sub, life_time_second: int):
    """Генерирует токен доступа.
    В качестве параметра sub нужно указать владельца.
    Например, в случае токена доступа для пользователя,
    в качестве sub нужно указать его id.
    Ещё пример. Если вы генерируете email confirmation token,
    то в качестве sub нужно передать почту.

    Также нужно указать, через сколько истекает токен.
    """
    timestamp = int(time.time())
    payload = {
        'iss': str(JWT_ISSUER),
        'iat': int(timestamp),
        'exp': int(timestamp + life_time_second),
        'sub': str(sub)
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise Unauthorized from e


def generate_confirmation_url(sub: str, end_point: str):
    """Генерирует ссылку для подтверждения чего угодно.
    Принимает конечную точку, которая обработает запрос на подтверждение,
    Название параметра в запросе: "token"
    """
    from urllib.parse import urlencode

    # URL-кодирование токена подтверждения электронной почты
    sub_confirmation_token = generate_token(sub, 15 * 60)
    encoded_token = urlencode({'token': sub_confirmation_token})

    # Генерация URL-адреса с кодированным токеном в качестве параметра запроса
    confirmation_url = f'{end_point}?{encoded_token}'

    return confirmation_url


def generate_password(length: int = 20):
    """Очень небезопансая функция, которая
    генерирует пароль указанной длины (по умолчанию 20)
    """
    import string
    import random

    all_chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_chars) for i in range(length))

    return password
