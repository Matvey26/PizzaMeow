from .base import Base
import getpass, os

class SignUp(Base):
    """Регистрация"""
    def run(self, session):
        email = self.options.email

        if '@' not in email:
            print('Неверный формат почты')
            return

        password = getpass.getpass('Введите пароль: ')
        check_password = getpass.getpass('Подтвердите пароль: ')
        if password != check_password:
            print(f'Введенные пароли не совпали, попробуйте еще раз')
            return

        answer = session.sign_up(email, password)
        if answer:
            print(answer[1])
            return
        
        print('Регистрация аккаунта была выполнена успешно. Теперь подтвердите почту.')
        print(f'На {email} было отправлено письмо с ссылкой для подтверждения почты.')
    

    