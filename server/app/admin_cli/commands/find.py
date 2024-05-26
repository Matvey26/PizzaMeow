from .base import Base


class Find(Base):
    """Найти запись по ключу"""

    def run(self):
        tablename = self.options.tablename
        kwargs = dict(self.options.key) if self.options.key else {}

        repository = self.repositories.get(tablename, None)
        if repository is None:
            print('Указано неверное имя таблицы.')
            return

        result = repository.find_by(**kwargs)

        print(result)
