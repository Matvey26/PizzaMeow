from .base import Base
import getpass 

class Entrance(Base):
    """Вход"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def __sign_in(email):
        check_password = 'написать получение верного пароля'
        password = getpass.getpass("Enter your password: ")
        while password != check_password:
            print(f'Введен неверный пароль, попробуйте еще раз')
            password = getpass.getpass("Enter your password: ")
        print('Вы успешно вошли в аккаунт')

    def run(self):
        self.__sign_in()