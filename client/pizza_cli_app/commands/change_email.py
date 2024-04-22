from .base import Base
from ..api.api import Session
import getpass


class ChangeEmail(Base):
    """Привязать к учётной записи другую почту."""

    def run(self, session: Session):
        old_email = self.options.old_email
        new_email = self.options.new_email
        password = getpass.getpass("Введите пароль: ")

        answer = session.change_email(old_email, password, new_email)
        if answer:
            print(answer[1])
            return
        
        print('Новая почта привязана к учётной записи.')
        print(f'На {new_email} было отправлено письмо с ссылкой для её подтверждения.')
