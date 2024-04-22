from . import user_repository
from flask import abort


def validate_email(email: str) -> bool:
    """Validate email"""
    if '@' not in email:
        return 'Неверный формат почты: отсутствует символ @'
    return 'OK'


def validate_password(password: str) -> bool:
    """Validate password"""
    if len(password) < 8:
        return 'Длина пароля должна быть не меньше 8 символов'
    return 'OK'


def sign_in(email: str, password: str) -> str:
    """Авторизация.
    
    Параметры
    ---------
    email: str
        Почта, которая привязана к аккаунту пользователя
    password: str
        Пароль от аккаунта пользователя

    Возвращает
    ----------
    access token: str
        Токен доступа от аккаунта пользователя
    """
    user = user_repository.get_by_email(email)
    if user is None:
        abort(404, 'Неверно указана почта или пароль')
    
    if user_repository.authenticate(email, password):
        from ..utils.auth import generate_token
        return generate_token(user.id, 24 * 60 * 60)
    
    abort(401, f'Неверный пароль от почты {email}')


def sign_up(body):
    """Регистрация. Возвращает access token"""

    email = body.get('email', '')
    password = body.get('password', '')

    validate = (validate_email(email), validate_password(password))
    if validate[0] != 'OK':
        abort(404, validate[0])
    
    if validate[1] != 'OK':
        abort(404, validate[1])

    user = user_repository.get_by_email(email)
    if user:
        abort(400, 'Это почта уже используется')
    

    # Создаём нового, неподтверждённого пользователя
    user = user_repository.create(email=email, password=password)
    user_repository.save(user)

    send_confirm_email(user.id, {}, email)

    return sign_in(email, password)


def send_confirm_email(user: str, token_info: dict, email: str):
    user_id = int(user)
    user = user_repository.get_by_email(email)
    if user.id != user_id:
        abort(401, 'Вы не можете запросить письмо с подтверждением почты для другого аккаунта')

    if user_repository.is_confirmed(user):
        abort(404, 'Аккаунт уже подтверждён')
    
    # Генерируем токен для подтверждения аккаунта
    from ..utils.auth import generate_token, generate_confirmation_url
    email_confirmation_token = generate_token(email, 15 * 60)
    confirm_email_end_point = 'http://127.0.0.1:8000/api/users/confirm'
    confirm_email_url = generate_confirmation_url(email_confirmation_token, confirm_email_end_point)

    # Отправляем письмо с просьбой подтвердить аккаунт
    from ..utils.send_email import send_email
    send_email(email, 'Подтверждение аккаунта', f'Перейдите по ссылке, чтобы подтвердить аккаунт. Ссылка истечёт через 15 минут {confirm_email_url}')


def confirm_email(email_confirmation_token):
    if not email_confirmation_token:
        abort(500, 'Ссылка на подтверждение почты недействительна')

    from ..utils.auth import decode_token
    email = decode_token(email_confirmation_token)['sub']
    
    user = user_repository.get_by_email(email)
    if not user_repository.is_confirmed(user):
        user_repository.mark_as_confirmed(user)
    user_repository.update(user)


def update_config(user: str, token_info: dict, body: dict):
    print('UPDATE_CONFIG', type(user))
    user_id = int(user)
    user = user_repository.get(user_id)
    firstname = body.get('firstname', '')
    lastname = body.get('lastname', '')
    address = body.get('address', '')
    phone = body.get('phone', '')

    if firstname:
        user.firstname = firstname
    if lastname:
        user.lastname = lastname
    if address:
        user.address = address
    if phone:
        user.phone_number = phone
    
    user_repository.update(user)


def change_password(user: int, token_info: dict, body: str):
    new_password = body
    user_id = int(user)
    user = user_repository.get(user_id)
    user_repository.change_password(user, new_password)
    user_repository.update(user)


def reset_password():
    pass