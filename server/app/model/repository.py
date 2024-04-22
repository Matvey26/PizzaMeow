from abc import ABC, abstractmethod

from sqlalchemy import desc

from ..database import db_session
from .models import Model

class Repository(ABC):
    """Этот класс содержит общие методы, которые
    используются для всех других классов-репозиториев.
    Подклассы могут предоставлять реалищацию этих методов.
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

        return self.session.query(self.__model_class).filter_by(id=model_id).first()

    def get_all(self) -> list:
        """Получает все модели этого класса, которые
        содержатся в базе данных.
        
        Возвращает
        ----------
        list :
            Список всех моделей, хранящихся в базе данных, упорядоченный по возрастанию их id.
        """

        return self.session.query(self.__model_class).order_by(desc(self.__model_class.id))

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
            Экземпляр, с обновлёнными значениями аттрибутов.
        """

        self.session.commit()

    def delete(self, model: Model) -> int:
        """Удаляет модель из базы данных.
        
        Параметры
        ---------
        model : Model
            Экземпляр модели, который нужно удалить.
        
        Возвращает
        ----------
        id : int
            Число - id объекта, который был удалён
        """

        deleted = self.session.delete(model)
        self.session.commit()

        return deleted

    @abstractmethod
    def is_invalid(self, model: Model) -> list:
        """Проверяет, является ли данный объект модели валидным.

        Параметры
        ---------
        model : Model
            Объект модели.

        Возвращает
        ----------
            list: Список, содержащий ошибки полей.
        """


        return []
