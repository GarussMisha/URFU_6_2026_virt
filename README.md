# Проект по виртуализации 

## Запуск проверта 
1. Установка виртуального окружения: `python -m venv venv`
2. Установка зависимостей `pip install -r requirements.txt`
3. Запуск Docker контейнера с PostgreSQL: `docker-compose up`


## Структура файлов
docker-compose.db.yaml - Развертывание БД Postgre на ВМ vm-pg001
.env - Переменные окружения для проекта (`PG_DATABASE_URL`, `FLASK_ENV`, `SECRET_KEY`)
