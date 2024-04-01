from .base import Base
import getpass

class Registration(Base):
    """Регистрация"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def __sign_in(self):
        email = self.options.email
        password = getpass.getpass("Enter your password: ")
        check_password = getpass.getpass("Confirm your password: ")
        while password != check_password:
            print(f'Введенные пароли не совпали, попробуйте еще раз')
            password = getpass.getpass("Enter your password: ")
            check_password = getpass.getpass("Confirm your password: ")
        print(f"Sign in with email: {email}, password: {len(password)} characters")

    def run(self):
        self.__sign_in()