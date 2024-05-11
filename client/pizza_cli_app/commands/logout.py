import asyncio
from .base import Base


class Logout(Base):
    """Выход из учётной записи."""

    async def run(self):
        self.session.logout()
