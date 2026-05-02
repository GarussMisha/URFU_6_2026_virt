from app import create_app, db # Импорт из __init__.py
import os

# Создаем экземпляр приложения, который уже настроен на подключение к БД!
app = create_app() 


if __name__ == '__main__':
    # Убедитесь, что переменная PG_DATABASE_URL установлена в вашей среде перед запуском!
    if not os.getenv('PG_DATABASE_URL'):
        print("ОШИБКА: Переменная окружения PG_DATABASE_URL не найдена. Проверьте .env.")
    else:
        with app.app_context():
            db.create_all() 

    app.run(debug=True) 