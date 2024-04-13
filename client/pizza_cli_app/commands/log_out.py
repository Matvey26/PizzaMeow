from .base import Base
import os

class Log_out(Base):
    """Ввод данных"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
    
    def run(self, session, token):
        del(token)
        if os.path.exists('token.bin'):
            os.remove('token.bin')
            print(f"Токен удален")