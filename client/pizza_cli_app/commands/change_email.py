import asyncio
import getpass

from .base import Base
from ..utils.print_format import load_spinner


class ChangeEmail(Base):
    """Привязать к учётной записи другую почту."""

    async def run(self):
        old_email = self.options.old_email
        new_email = self.options.new_email
        password = getpass.getpass("Введите пароль: ")

        task_load = asyncio.create_task(load_spinner())
        task_change_email = asyncio.create_task(
            self.session.change_email(old_email, password, new_email)
        )

        answer = await task_change_email
        task_load.cancel()

        if answer:
            print(answer[1])
            return

        print('Новая почта привязана к учётной записи.')
        print(
            f'На {new_email} было отправлено '
            'письмо с ссылкой для её подтверждения.'
        )
