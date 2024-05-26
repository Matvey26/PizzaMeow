from .base import Base


class Delete(Base):
    def run(self):
        tablename = self.options.tablename
        id = self.options.id

        repository = self.repositories.get(tablename, None)
        if repository is None:
            print('Указано неверное имя таблицы.')
            return

        if id == -1:
            answer = input(f'Вы точно хотите удалить ВСЕ записи таблицы {tablename}? (Y/n): ')
            if answer != 'Y':
                print('Прерываю удаление.')
                return
            i = 1
            while True:
                try:
                    record = repository.get(i)
                    repository.delete(record)
                except Exception:
                    break
                i += 1
            print('Все записи успешно удалены.')
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
            answer = input(f'Вы точно хотите удалить запись из '
                           f'таблицы {tablename} с индексом {id}? (Y/n): ')
            if answer == 'Y':
                repository.delete(record)
            else:
                print('Прерываю удаление')
                return
        except Exception as e:
            print('При удалении возникли ошибки.')
            print(e)
            return

        print('Запись успешно удалена.')
