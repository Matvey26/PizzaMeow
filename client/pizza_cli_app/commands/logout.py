from .base import Base
import os

class Logout(Base):
    """Ввод данных"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
    
    def run(self, session):
        session.logout()