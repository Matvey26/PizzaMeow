import asyncio

from .base import Base
from ..utils.print_format import load_spinner


class GetConfirmEmail(Base):
    async def run(self):
        email = self.options.email

        task_load = asyncio.create_task(load_spinner())
        task_confirm_email = asyncio.create_task(
            self.session.confirm_email(email)
        )

        response = await task_confirm_email
        task_load.cancel()

        if isinstance(response, tuple):
            print(response[1])
            return

        print(f'Письмо отправлено на почту {email}')
