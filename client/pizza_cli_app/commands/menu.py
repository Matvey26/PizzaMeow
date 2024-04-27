from .base import Base


class Menu(Base):
    """Команда для вывода меню пиццы"""

    def run(self, session):
        show_id = self.options.show_id

        raise NotImplementedError('Команда menu ещё не реализована.')
        
