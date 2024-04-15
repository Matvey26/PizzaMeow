class Menu:
    """Команда для вывода меню пиццы"""

    def __init__(self, args):
        self.args = args

    def run(self, session):
        show_id = self.args.show_id

        raise NotImplementedError('Команда menu ещё не реализована.')
        
