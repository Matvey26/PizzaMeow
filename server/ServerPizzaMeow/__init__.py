import connexion
from connexion import FlaskApp

def create_app():
	connex_app = connexion.App(__name__, specification_dir='./')
	connex_app.add_api("swagger.yml")

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


connex_app = create_app()