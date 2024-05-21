import asyncio
from .base import Base
import getpass


class ChangePasssword(Base):
    """Востановление пароля"""

    async def run(self):
        email = self.options.email
        old_password = getpass.getpass('Введите текущий пароль: ')
        new_password = getpass.getpass('Введите новый пароль: ')
        check_new_password = getpass.getpass('Подтвердите новый пароль: ')
        if new_password != check_new_password:
            print('Введенные пароли не совпали, попробуйте еще раз')
            return

        task_load = asyncio.create_task(self.load_spinner())
        task_change_password = asyncio.create_task(
            self.session.change_password(
                email,
                old_password,
                new_password
            )
        )

        answer = await task_change_password
        task_load.cancel()

        if answer:
            print(answer[1])
            return
        print('Вы успешно сменили пароль.')
