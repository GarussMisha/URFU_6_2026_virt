# План реализации проекта CRUD

## 1. Выбор стека технологий
- **Язык/фреймворк**: Python + Flask (уже присутствует в проекте).
- **База данных**: PostgreSQL в Docker‑контейнере (уже есть `docker-compose.yml`).
- **Object Storage**: MinIO (локальный S3‑совместимый сервис в Docker).
- **Балансировщик нагрузки**: Nginx в отдельном контейнере, конфигурируемый через Terraform.
- **Infrastructure as Code**: Terraform для развертывания всех ресурсов в Yandex.Cloud (VPC, подсети, балансировщик, контейнеры, Object Storage, Serverless‑функции).
- **Serverless‑компоненты**: Yandex Cloud Functions (пример: обработка загрузки файлов в Object Storage).

## 2. Структура проекта
```
Project/
├─ app/                     # Flask‑приложение
│  ├─ __init__.py          # инициализация Flask и SQLAlchemy
│  ├─ config.py            # конфигурация (DB, MinIO, etc.)
│  ├─ models.py            # модели SQLAlchemy (CRUD‑сущности)
│  ├─ routes.py            # CRUD‑эндпоинты
│  └─ utils.py             # вспомогательные функции (например, работа с MinIO)
├─ infra/                   # Terraform‑модули
│  ├─ main.tf
│  ├─ variables.tf
│  └─ outputs.tf
├─ docker-compose.yml       # локальная инфраструктура (Postgres, MinIO, Nginx)
├─ requirements.txt         # Python‑зависимости
├─ run.py                   # точка входа Flask‑приложения
├─ docs/Task.md            # требования к проекту
└─ plans/todo.md           # текущий план (это файл)
```

## 3. План работ (TODO‑лист)
1. **Настроить конфигурацию**
   - Заполнить `app/config.py` параметрами подключения к PostgreSQL и MinIO (чтение из переменных окружения).
2. **Определить модели**
   - В `app/models.py` создать SQLAlchemy‑модель, например `Item` с полями `id`, `name`, `description`, `created_at`.
3. **Реализовать CRUD‑эндпоинты**
   - В `app/routes.py` добавить маршруты:
     - `POST /items` – создание записи.
     - `GET /items` – список всех записей.
     - `GET /items/<id>` – получение конкретной записи.
     - `PUT /items/<id>` – обновление записи.
     - `DELETE /items/<id>` – удаление записи.
4. **Подключить Object Storage**
   - Добавить `utils.py` с функциями загрузки/получения файлов в MinIO.
   - Добавить эндпоинт `POST /items/<id>/file` для загрузки файлов, сохраняющих ссылки в модели.
5. **Docker‑инфраструктура**
   - Обновить `docker-compose.yml`:
     - Сервис `postgres` с томом для персистентности.
     - Сервис `minio` (S3‑совместимый) с томом.
     - Сервис `nginx` как обратный прокси/балансировщик.
6. **Terraform‑скрипты**
   - Создать `infra/main.tf` с ресурсами Yandex.Cloud:
     - VPC, подсети, правила firewall.
     - Managed PostgreSQL кластер.
     - Object Storage bucket.
     - Load Balancer (target‑group + listener).
     - Serverless‑функцию, вызываемую при загрузке файлов.
   - Добавить переменные и outputs.
7. **CI/CD (опционально)**
   - Настроить GitHub Actions для сборки Docker‑образов и применения Terraform.
8. **Тестирование**
   - Написать unit‑тесты для CRUD‑операций (pytest + Flask‑testing).
   - Проверить работу с MinIO и балансировщиком.
9. **Документация**
   - Обновить `README.md` с инструкциями по локальному запуску и деплою в Yandex.Cloud.
10. **Мониторинг и логирование**
    - Включить Cloud Logging и Yandex Monitoring в Terraform‑конфигурацию.
    - Добавить базовый health‑check эндпоинт `/health`.

## 4. Последовательность выполнения
1. Заполнить конфигурацию и зависимости.
2. Реализовать модели и CRUD‑эндпоинты.
3. Добавить работу с Object Storage.
4. Настроить локальный Docker‑стек и убедиться в работе приложения.
5. Перенести инфраструктуру в Terraform и задеплоить в Yandex.Cloud.
6. Добавить серверлесс‑функцию и настроить балансировщик.
7. Тестировать, документировать и настроить мониторинг.

---

**Следующий шаг** – согласовать план. Если требуется изменить порядок, добавить/убрать задачи, дайте знать.

