from ..api.api import Session


class Base:
    """Базовая команда"""

    def __init__(self, options, session: Session):
        self.options = options
        self.session = session

    def run(self):
        raise NotImplementedError('You must implement the run() method!')
