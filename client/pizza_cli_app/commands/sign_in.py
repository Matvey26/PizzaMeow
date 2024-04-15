from .base import Base
import getpass, os

class SignIn(Base):
    """Вход"""
    def run(self, session):
        email = self.options.email

        password = getpass.getpass("Введите пароль: ")
        answer = session.sign_in(email, password)
        if answer:
            print(answer[1])
            return
        
        print('Вход в аккаунт выполнен успешно.')