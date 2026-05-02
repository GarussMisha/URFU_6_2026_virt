import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # 1. Настройка конфигурации БД из переменных окружения (читаем .env)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('PG_DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 2. Инициализация SQLAlchemy
    db.init_app(app)

    # 3. Регистрация роутов
    from . import routes
    
    return app


# Примечание: В дальнейшем вы будете вызывать create_app() в run.py
