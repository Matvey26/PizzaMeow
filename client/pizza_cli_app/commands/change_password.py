from .base import Base
import getpass

class ChangePasssword(Base):
    """Востановление пароля"""
    def run(self, session):
        email = self.options.email
        old_password = getpass.getpass('Введите текущий пароль: ')
        new_password = getpass.getpass('Введите новый пароль: ')
        check_password = getpass.getpass('Подтвердите пароль: ')
        if new_password != check_password:
            print(f'Введенные пароли не совпали, попробуйте еще раз')
            return

        answer = session.change_password(email, old_password, new_password)
        if answer:
            print(answer[1])
            return
        print('Вы успешно сменили пароль.')