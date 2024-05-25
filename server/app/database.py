from connexion import FlaskApp

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = None
engine = None
db_session = None


def init(connex_app: FlaskApp):
    """Эта функция инициализирует SQLAlchemy ORM.

    В глобальные переменные Base, engine и db_session этого модуля
    помещаются базовый декларативный класс, "двигатель" sqlalchemy
    и текущая сессия соответственно.

    Параметры
    ---------
    connex_app : connexion.FlaskApp
        Приложение, для которого настраивается БД
        и которое было создано посредством connexion.App(...)
    """

    # получаем Flask приложение для настройки
    app = connex_app.app

    global Base, engine, db_session
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    # создаём новую сессию
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))

    # Расширения declarative в SQLAlchemy позволяет
    # определять таблицы и модели одновременно
    Base = declarative_base()
    Base.query = db_session.query_property()

    # прикрепляем функцию shutdown_session,
    # которая будет автоматически завершать сессию
    app.teardown_appcontext(shutdown_session)


def shutdown_session(exception=None) -> None:
    """Завершает сессию SQLAlchemy."""

    db_session.remove()
