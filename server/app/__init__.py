from flask import Flask
import connexion

def create_app(test_config: dict = {}):
	app = connexion.App(__name__, specification_dir='./')
	app.add_api("swagger.yml")

	load_config(app, test_config)

	return app


def load_config(app: Flask, test_config: dict) -> None:
	pass


def init_database(app: Flask) -> None:
	from database import init
	init(app)


app = create_app()

@app.route('/')
def helloworld():
	return "Hello World"

if __name__ == "__main__":
	app.run(host='0.0.0.0', port='8000')