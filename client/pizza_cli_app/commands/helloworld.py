from .base import Base

class HelloWorld(Base):
    """Just say 'Hello World'"""

    def run(self):
        print("Hello, World!")