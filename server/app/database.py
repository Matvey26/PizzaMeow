from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = None

def init(app: Flask):
    """Запускает базу данных"""
    global db

    pass
