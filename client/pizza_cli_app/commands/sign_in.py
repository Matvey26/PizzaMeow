import asyncio
import getpass

from .base import Base
from ..utils.print_format import load_spinner


class SignIn(Base):
    """Вход"""

    async def run(self):
        email = self.options.email

        password = getpass.getpass("Введите пароль: ")

        task_load = asyncio.create_task(load_spinner())
        task_signin = asyncio.create_task(
            self.session.sign_in(email, password))

        answer = await task_signin
        task_load.cancel()

        if answer:
            print(answer[1])
            return

        print('Вход в аккаунт выполнен успешно.')
