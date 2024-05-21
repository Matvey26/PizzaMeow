from .base import Base


class Create(Base):
    """Создаёт новую запись в таблице.
    Имена таблиц следующие: user, pizza, payment, order, order_item, cart, cart_item.
    Чтобы узнать аргументы для создания, запустите команду без именованных аргументов.
    """

    def run(self):
        tablename = self.options.tablename
        kwargs = dict(self.options.key) if self.options.key else {}

        repository = self.repositories.get(tablename, None)
        if repository is None:
            print('Указано неверное имя таблицы.')
            return

        try:
            record = repository.create(**kwargs)
        except Exception as e:
            print('При создании произошла ошибка. Возможно, вы указали неверные аргументы.')
            print(e)
            return

        try:
            repository.save(record)
        except Exception as e:
            print('Произошла ошибка. Не удалось сохранить запись.')
            print(e)
            return

        print('Запись успешно сохранена.')
