from .base import Base


class Logout(Base):
    """Выход из учётной записи."""

    def run(self):
        self.session.logout()
