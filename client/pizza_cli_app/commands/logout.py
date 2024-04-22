from .base import Base
import os

class Logout(Base):
    """Выход из учётной записи."""
    
    def run(self, session):
        session.logout()