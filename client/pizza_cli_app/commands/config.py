import asyncio
from .base import Base


class Config(Base):
    """Ввод/обновление данных."""

    async def run(self):
        firstname = self.options.firstname
        lastname = self.options.lastname
        address = self.options.address
        phone = self.options.phone

        answer = ''

        data = {}
        if firstname:
            data['firstname'] = firstname
            answer += f'Имя успешно обновлено на {firstname}\n'
        if lastname:
            data['lastname'] = lastname
            answer += f'Фамилия успешно обновлена на {lastname}\n'
        if address:
            data['address'] = address
            answer += f'Адрес успешно обновлен на {address}\n'
        if phone:
            data['phone'] = phone
            answer += f'Номер телефона успешно обновлен на {phone}\n'


        task_load = asyncio.create_task(self.load_spinner())
        task_config = asyncio.create_task(self.session.config(data))

        response = await task_config
        task_load.cancel()

        if response:
            print(response[1])
            return

        print(answer.rstrip())
