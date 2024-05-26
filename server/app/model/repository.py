from abc import ABC
from sqlalchemy import desc
from ..database import db_session
from .models import Model


class Repository(ABC):
    """Этот класс содержит общие методы, которые
    используются для всех других классов-репозиториев.
    Подклассы могут предоставлять реализацию этих методов.
    """

    def __init__(self, model_class):
        self.__model_class = model_class
        self.session = db_session

    def get(self, model_id: int) -> Model:
        """Получает модель из базы данных по id.

        Параметры
        ---------
        model_id : int
            Целое число, айди записи, которую вы хотите получить.

        Возвращает
        ----------
        Model
            Модель, если в базе данных есть модель с таким id.
        None
            Ничего, если модели с таким id нет.
        """

        return self.session.query(self.__model_class).filter_by(
            id=model_id
        ).first()

    def get_all(self) -> list:
        """Получает все модели этого класса, которые
        содержатся в базе данных.

        Возвращает
        ----------
        list :
            Список всех моделей, хранящихся в базе данных,
            упорядоченный по возрастанию их id.
        """

        return self.session.query(self.__model_class).order_by(
            desc(self.__model_class.id)
        ).all()

    def get_page(self, offset: int, limit: int) -> tuple:
        return self.session.query(self.__model_class).offset(offset).limit(limit).all()

    def save(self, model: Model) -> None:
        """Сохраняет модель в базе данных.

        Параметры
        ---------
        model : Model
            Модель, которую нужно сохранить.
        """

        self.session.add(model)
        self.session.commit()

    def update(self, model: Model) -> None:
        """Обновляет существующую модель в базе данных.

        Параметры
        ---------
        model : Model
            Экземпляр, с обновлёнными значениями атрибутов.
        """

        self.session.commit()

    def delete(self, model: Model) -> None:
        """Удаляет модель из базы данных.

        Параметры
        ---------
        model : Model
            Экземпляр модели, который нужно удалить.
        """

        self.session.delete(model)
        self.session.commit()

    def serialize(self, *models: Model) -> dict:
        """Сериализация объекта.

        Параметры
        ---------
        model : Model
            Экземпляр модели, который нужно сериализовать.

        Возвращает
        ----------
        dict
            Сериализованный объект
        """
        serialized = []
        for model in models:
            serialized.append(model.serialize())

        return serialized

    def find_by(self, **kwargs) -> list:
        """Ищет записи по указанным ключам и значениям.

        Параметры
        ---------
        **kwargs
            Ключи и значения, по которым нужно искать записи.

        Возвращает
        ----------
        list :
            Список найденных записей, удовлетворяющих условиям поиска.
        """
        try:
            return self.session.query(self.__model_class).filter_by(
                **kwargs
            ).all()
        except AttributeError as e:
            print(f"Error: {e}")
            print("One or more keys are not valid attributes of the model.")
            return []
