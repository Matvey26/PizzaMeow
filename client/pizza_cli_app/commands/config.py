from .base import Base

class Config(Base):
    """Ввод данных"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
    
    def run(self, session, token):
        print(f"{self.options}")