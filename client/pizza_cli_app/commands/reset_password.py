from .base import Base


class ResetPasssword(Base):
    """Востановление пароля"""

    def run(self):
        email = self.options.email
        answer = self.session.reset_password(email)
        if answer:
            print(answer[1])
            return
        print('Письмо для сброса пароля отправлено на указанную почту.')
