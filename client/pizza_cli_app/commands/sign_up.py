import asyncio
import getpass

from .base import Base
from ..utils.print_format import load_spinner


class SignUp(Base):
    """Регистрация"""

    async def run(self):
        email = self.options.email

        if '@' not in email:
            print('Неверный формат почты')
            return

        password = getpass.getpass('Введите пароль: ')
        check_password = getpass.getpass('Подтвердите пароль: ')
        if password != check_password:
            print('Введенные пароли не совпали, попробуйте еще раз')
            return

        task_load = asyncio.create_task(load_spinner())
        task_sign_up = asyncio.create_task(
            self.session.sign_up(email, password))

        answer = await task_sign_up
        task_load.cancel()

        if answer:
            print(answer[1])
            return

        print('Регистрация аккаунта была выполнена '
              'успешно. Теперь подтвердите почту.')
        print(f'Проверьте свою почту: {email}. На неё было '
              'отправлено письмо с ссылкой для подтверждения почты.')
