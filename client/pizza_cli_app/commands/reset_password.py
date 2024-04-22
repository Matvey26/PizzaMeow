from .base import Base

class ResetPasssword(Base):
    """Востановление пароля"""
    def run(self, session):
        email = self.options.email
        answer = session.reset_password(email)
        if answer:
            print(answer[1])
            return
        print('Письмо для сброса пароля отправлено на указанную почту.')