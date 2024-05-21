import asyncio

from .base import Base
from ..utils.print_format import load_spinner


class ResetPasssword(Base):
    """Востановление пароля"""

    async def run(self):
        email = self.options.email

        task_load = asyncio.create_task(load_spinner())
        task_reset_password = asyncio.create_task(
            self.session.reset_password(email)
        )

        answer = await task_reset_password
        task_load.cancel()

        if answer:
            print(answer[1])
            return
        print('Письмо для сброса пароля отправлено на указанную почту.')
