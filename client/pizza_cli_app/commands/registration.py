from .base import Base
import getpass, os

class Registration(Base):
    """Регистрация"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def __sign_in(self, session):
        email = self.options.email
        password = getpass.getpass("Enter your password: ")
        check_password = getpass.getpass("Confirm your password: ")
        while password != check_password:
            print(f'Введенные пароли не совпали, попробуйте еще раз')
            password = getpass.getpass("Enter your password: ")
            check_password = getpass.getpass("Confirm your password: ")
        print(f"Sign in with email: {email}, password: {len(password)} characters")
        token = session.sign_up(email, password)
        if type(token) == tuple:
            print('Неверный пароль')
        elif token == -1:
            print('Подключение прошло не успешно')
        else:
            print('Успешное подключение')
            self.__create_file(token)
        
    def __create_file(self, token):
        if not os.path.exists('your_token'):
            with open('your_token.bin', 'w') as file:
                file.write(token)
            print(f"Токен сохранен")
        else:
            os.remove('token.bin')
            with open('your_token.bin', 'w') as file:
                file.write(token)
            print(f"Токен сохранен")

    def run(self, session, token):
        return self.__sign_in(session)
    

    