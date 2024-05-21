from .base import Base


class Delete(Base):
    def run(self):
        tablename = self.options.tablename
        id = self.options.id

        repository = self.repositories.get(tablename, None)
        if repository is None:
            print('Указано неверное имя таблицы.')
            return

        try:
            record = repository.get(id)
        except Exception as e:
            print('Запись не найдена.')
            print(e)
            return

        if record is None:
            print('Запись не найдена.')
            return

        try:
            repository.delete(record)
        except Exception as e:
            print('При удалении возникли ошибки.')
            print(e)
            return

        print('Запись успешно удалена.')
