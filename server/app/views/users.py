import json

PATH = 'server/database/users.json'


def open_db() -> dict:
    with open(PATH) as db:
        return json.load(db)


DATA = open_db()


def validate_email(email: str) -> bool:
    """Validate email"""
    return True


def validate_password(password: str) -> bool:
    """Validate password"""
    return True


def add(new_user: dict):
    DATA['UNUSED_ID'] += 1
    DATA['USERS'][str(new_user['id'])] = new_user


def commit():
    with open(PATH, 'w') as db:
        json.dump(DATA, db)


def register(body):
    email = body.get('email', '')
    password = body.get('password', '')
    """Регистрирует нового пользователя и возвращает его access token"""
    # Валидируем данные
    if not validate_email(email):
        pass  # Тут надо как-то вызвать исключение, но я чёт пока не понял как
    if not validate_password(password):
        pass  # А тут надо вызвать уже другое исключение, что пароль небезопасный

    # Создаём нового пользователя
    user_id = DATA['UNUSED_ID']
    new_user = {
        'id': user_id,
        'email': email,
        'password': password
    }

    # Добавляем пользователя в "базу данных"
    add(new_user)
    commit()

    from .auth import generate_token
    return generate_token(user_id)


def get_user_info(user, token_info):
    USER = DATA['USERS'][str(user)]
    print(USER)
    answer = {
        'id': user,
        'firstname': USER.get('firstname', 'None'),
        'lastname': USER.get('lastname', 'None')
    }
    return answer