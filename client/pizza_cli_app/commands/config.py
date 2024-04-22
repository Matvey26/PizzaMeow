from .base import Base
from ..api.api import Session


class Config(Base):
    """Ввод/обновление данных."""
        
    def run(self, session: Session):
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
        
        response = session.config(data)
        if response:
            print(response[1])
            return
        
        print(answer.rstrip())
        