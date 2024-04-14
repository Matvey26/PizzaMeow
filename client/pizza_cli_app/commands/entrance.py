from .base import Base
import getpass, os

class Entrance(Base):
    """Вход"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def __sign_in(self, session):
        email = self.options.email
        password = getpass.getpass("Enter your password: ")
        token = session.sign_in(email, password)
        while type(token) == tuple or token == -1:
            if type(token) == tuple:
                print(f'Введен неверный пароль, попробуйте еще раз')
            elif token == -1:
                print('Подключение прошло не успешно')
            else:
                print('Вы успешно вошли в аккаунт')
                print(f'токен = {token}')
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