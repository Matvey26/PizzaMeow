class Menu:
    """Команда для вывода меню пиццы"""

    def __init__(self, args):
        self.args = args

    def run(self, session):
        show_id = self.args.show_id

        # Загружаем все меню пиццы с сервера
        menu = session.get_all_pizza_menu()

        # Выводим меню на экран
        for i, item in enumerate(menu, 1):
            if show_id:
                print(f'{item["id"]}. {item["name"]} - {item["price"]}')
            else:
                print(f'{i}. {item["name"]} - {item["price"]}')
