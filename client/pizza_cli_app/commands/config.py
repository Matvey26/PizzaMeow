from .base import Base

class Config(Base):
    """Вход"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        print(f"{self.args}")