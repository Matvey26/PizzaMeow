from . import user_repository
from flask import abort
import os


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
        abort(404, 'Аккаунта с такой почтой не существует. '
              'Проверьте правильность ввода или зарегистрируйтесь.')

    if user_repository.authenticate(email, password):
        from ..utils.auth import generate_token
        return generate_token(user.id, 24 * 60 * 60)

    abort(401, 'Введён неверный пароль. Пожалуйста, '
          'проверьте правильность ввода или восстановите пароль.')


def sign_up(body):
    """Регистрация. Возвращает access token"""

    email = body.get('email', '')
    password = body.get('password', '')

    validate = (validate_email(email), validate_password(password))
    if validate[0] != 'OK':
        abort(400, validate[0])

    if validate[1] != 'OK':
        abort(400, validate[1])

    user = user_repository.get_by_email(email)
    if user:
        abort(400, 'Это почта уже используется')

    try:
        send_confirm_email(email)
    except Exception:
        abort(400, 'Невозможно отправить письмо на указанную почту.')

    # Создаём нового, неподтверждённого пользователя
    user = user_repository.create(email=email, password=password)
    user_repository.save(user)

    return sign_in(email, password)


def send_confirm_email(email: str):
    # Генерируем токен для подтверждения аккаунта
    from ..utils.auth import generate_confirmation_url
    confirm_email_end_point = os.environ['SERVER_URL'] + 'api/users/confirm'
    confirm_email_url = generate_confirmation_url(
        email, confirm_email_end_point)

    # Отправляем письмо с просьбой подтвердить аккаунт
    from ..utils.send_email import send_email
    send_email(
        email,
        'Подтверждение аккаунта',
        'Перейдите по ссылке, чтобы подтвердить аккаунт. '
        f'Ссылка истечёт через 15 минут {confirm_email_url}'
    )


def get_confirm_email(user: str, token_info: dict, email: str):
    email = email.decode() if isinstance(email, bytes) else email
    user_id = int(user)
    user = user_repository.get_by_email(email)
    if user is None:
        abort(400, 'Токен недействителен.')
    if user.id != user_id:
        abort(
            401,
            'Вы не можете запросить письмо с '
            'подтверждением почты для другого аккаунта'
        )

    if user_repository.is_confirmed(user):
        abort(400, 'Аккаунт уже подтверждён')

    send_confirm_email(email)


def confirm_email(token):
    if not token:
        abort(500, 'Ссылка на подтверждение почты недействительна')

    from ..utils.auth import decode_token
    email = decode_token(token)['sub']

    user = user_repository.get_by_email(email)
    if not user_repository.is_confirmed(user):
        user_repository.mark_as_confirmed(user)
    user_repository.update(user)


def update_config(user: str, token_info: dict, body: dict):
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


def change_password(user: str, token_info: dict, body: str):
    """Изменяет пароль пользователя.
    Параметры
    ---------
    user : str
        Айди пользователя
    token_info : dict
        Этот параметр нужен для connexion, фактически бесполезен
    body : str
        Электронная почта пользователя
    """
    new_password = body.decode() if isinstance(body, bytes) else body
    user_id = int(user)
    user = user_repository.get(user_id)
    user_repository.change_password(user, new_password)
    user_repository.update(user)


def reset_password(body):
    email = body.decode() if isinstance(body, bytes) else body

    from ..utils.auth import generate_password
    from ..utils.send_email import send_email

    user = user_repository.get_by_email(email)

    if user is None:
        abort(
            400,
            'Учётной записи с такой почтой нет. Проверьте правильность ввода.'
        )

    new_password = generate_password()
    change_password(user.id, {}, new_password)
    send_email(
        email,
        'Изменение пароля',
        'Вы запросили изменение пароля. '
        f'Вот ваш новый пароль: {new_password}'
    )


def change_email(user: str, token_info: dict, body):
    user_id = int(user)
    new_email = body.decode() if isinstance(body, bytes) else body

    if user_repository.get_by_email(new_email) is not None:
        abort(400, 'Эта почта уже используется.')

    validate = validate_email(new_email)
    if validate != 'OK':
        abort(400, 'Неверный формат почты.')

    user = user_repository.get(user_id)

    user_repository.change_email(user, new_email)
    user_repository.update(user)

    send_confirm_email(new_email)


def delete_user(user, token_info):
    user_id = int(user)
    user = user_repository.get(user_id)
    user_repository.delete(user)
