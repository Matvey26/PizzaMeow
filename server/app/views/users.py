def validate_email(email: str) -> bool:
    """Validate email"""
    return True


def validate_password(password: str) -> bool:
    """Validate password"""
    return True


def register(body):
    email = body.get('email', '')
    password = body.get('password', '')
    
    from .auth import generate_token
    return generate_token(2)


def get_user_info(user, token_info):
    answer = {
        'id': user,
        'firstname': 'asd',
        'lastname': 'xcv'
    }
    return answer