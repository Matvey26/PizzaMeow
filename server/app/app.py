import connexion
from connexion import FlaskApp
import pathlib
import os


def create_app():
    base_dir = pathlib.Path(__file__).parent.resolve()
    connex_app = connexion.App(__name__, specification_dir=base_dir)
    connex_app.add_api("swagger.yml")

    app_dir = os.path.dirname(os.path.abspath(__file__))
    server_dir = os.path.dirname(app_dir)
    db_path = os.path.join(server_dir, 'pizza_db.sqlite')

    connex_app.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    print(connex_app.app.config['SQLALCHEMY_DATABASE_URI'])

    init_database(connex_app)

    return connex_app


def init_database(connex_app: FlaskApp) -> None:
    """Отвечает за инициализацию и создание баз данных, которыми будет
    пользоваться приложение

    Параметры
    ---------
    connex_app : connexion.FlaskApp
            Экземпляр приложения, которое будет запущено
    """
    from .database import init
    init(connex_app)


os.environ['SERVER_URL'] = 'http://127.0.0.1:8000/'
connex_app = create_app()
