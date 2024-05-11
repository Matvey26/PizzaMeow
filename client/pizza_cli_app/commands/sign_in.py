from .base import Base
import getpass


class SignIn(Base):
    """Вход"""

    def run(self):
        email = self.options.email

        password = getpass.getpass("Введите пароль: ")
        answer = self.session.sign_in(email, password)
        if answer:
            print(answer[1])
            return

        print('Вход в аккаунт выполнен успешно.')
