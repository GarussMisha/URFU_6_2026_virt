# Проект по виртуализации

## Описание
Приложение для управления складом товаров с использованием Flask, SQLAlchemy и PostgreSQL. Позволяет добавлять, редактировать, удалять и искать товары по ID.

## Запуск проекта
1. Установка виртуального окружения: `python -m venv venv`
2. Установка зависимостей: `pip install -r requirements.txt`
3. Развертывание базы данных (Docker): `docker-compose up -d`
4. Запуск приложения: `python run.py`

## Структура проекта

### Корневая директория
- [`run.py`](run.py:1) — Точка входа для запуска Flask-приложения.
- [`requirements.txt`](requirements.txt:1) — Список необходимых Python-пакетов.
- [`docker-compose.yml`](docker-compose.yml:1) — Конфигурация Docker Compose для оркестрации сервисов.
- [`docker-compose.db.yaml`](docker-compose.db.yaml:1) — Специфичный файл конфигурации для развертывания БД PostgreSQL на виртуальной машине.
- [`.env`](.env:1) — Файл с переменными окружения (конфиденциальные данные).

### Директория `app/` (Основной код приложения)
- [`app/__init__.py`](app/__init__.py:1) — Инициализация Flask-приложения и расширений.
- [`app/models.py`](app/models.py:1) — Определение моделей базы данных (SQLAlchemy).
- [`app/routes.py`](app/routes.py:1) — Обработка HTTP-запросов и маршрутизация API.
- [`app/config.py`](app/config.py:1) — Конфигурация приложения.

### Директория `app/templates/` (HTML шаблоны)
- [`app/templates/base.html`](app/templates/base.html:1) — Базовый шаблон с общей структурой сайта.
- [`app/templates/index.html`](app/templates/index.html:1) — Главная страница со списком товаров и формами управления.

### Директория `app/static/` (Статические файлы)
- [`app/static/style.css`](app/static/style.css:1) — Стили оформления интерфейса.
