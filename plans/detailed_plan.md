# Детальное описание шагов реализации CRUD‑проекта

## 1️⃣ Настройка конфигурации (`app/config.py`)
1. **Импортировать `os`** и создать класс `Config`.
2. **Переменные окружения** (читаются из `.env`):
   - `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT` → формируют `SQLALCHEMY_DATABASE_URI`.
   - `MINIO_ENDPOINT`, `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`, `MINIO_BUCKET` → параметры доступа к MinIO.
3. **Пример кода**:
   ```python
   import os

   class Config:
       SQLALCHEMY_DATABASE_URI = (
           f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
           f"{os.getenv('POSTGRES_HOST', 'postgres')}:{os.getenv('POSTGRES_PORT', '5432')}/"
           f"{os.getenv('POSTGRES_DB')}"
       )
       SQLALCHEMY_TRACK_MODIFICATIONS = False

       MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'http://minio:9000')
       MINIO_ACCESS_KEY = os.getenv('MINIO_ROOT_USER')
       MINIO_SECRET_KEY = os.getenv('MINIO_ROOT_PASSWORD')
       MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'uploads')
   ```
4. **Подключить конфиг** в `app/__init__.py`:
   ```python
   from .config import Config
   app = Flask(__name__)
   app.config.from_object(Config)
   ```

## 2️⃣ Определение моделей (`app/models.py`)
1. **Импортировать `db`** из `app/__init__.py`.
2. **Создать модель `Item`**:
   ```python
   from datetime import datetime
   from . import db

   class Item(db.Model):
       __tablename__ = "items"
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(120), unique=True, nullable=False)
       description = db.Column(db.Text, nullable=True)
       created_at = db.Column(db.DateTime, default=datetime.utcnow)
       file_url = db.Column(db.String(255), nullable=True)  # ссылка на файл в MinIO
   ```
3. **Инициализация БД** – добавить функцию `init_db()` в конец файла, вызываемую из `run.py` при первом старте.

## 3️⃣ CRUD‑эндпоинты (`app/routes.py`)
1. **Создать Blueprint** `items_bp` и зарегистрировать его в `app/__init__.py`.
2. **Эндпоинты**:
   - `POST /items` – создать запись.
   - `GET /items` – список всех записей.
   - `GET /items/<int:id>` – получить одну запись.
   - `PUT /items/<int:id>` – обновить запись.
   - `DELETE /items/<int:id>` – удалить запись.
3. **Обработка ошибок** – вернуть JSON с `message` и соответствующим HTTP‑статусом (400, 404).
4. **Пример кода** (частичный):
   ```python
   @items_bp.route('/items', methods=['POST'])
   def create_item():
       data = request.get_json()
       item = Item(name=data['name'], description=data.get('description'))
       db.session.add(item)
       db.session.commit()
       return jsonify(id=item.id), 201
   ```

## 4️⃣ Работа с Object Storage (MinIO) (`app/utils.py` и роуты)
1. **Создать `app/utils.py`**.
2. **Инициализировать клиент Boto3**:
   ```python
   import boto3
   from .config import Config

   minio_client = boto3.client(
       's3',
       endpoint_url=Config.MINIO_ENDPOINT,
       aws_access_key_id=Config.MINIO_ACCESS_KEY,
       aws_secret_access_key=Config.MINIO_SECRET_KEY,
   )
   ```
3. **Функция `upload_file(file_obj, filename)`** – загружает объект в бакет `Config.MINIO_BUCKET` и возвращает публичный URL.
4. **Эндпоинт загрузки** `POST /items/<int:id>/file` в `routes.py`:
   - Принимает `multipart/form-data`.
   - Вызывает `utils.upload_file`.
   - Сохраняет полученный URL в поле `file_url` модели `Item`.
5. **Эндпоинт получения** `GET /items/<int:id>/file` – редирект (`302`) на сохранённый URL.

## 5️⃣ Docker‑Compose локальная инфраструктура (`docker-compose.yml`)
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - pg_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  minio:
    image: minio/minio
    command: server /data
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    depends_on:
      - app

  app:
    build: .
    environment:
      - FLASK_ENV=development
    ports:
      - "5000:5000"
    depends_on:
      - postgres
      - minio

volumes:
  pg_data:
  minio_data:
```
Том `pg_data` и `minio_data` обеспечивают персистентность.

## 6️⃣ Terraform‑инфраструктура (`infra/`)
### 6.1 `main.tf`
```hcl
provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.yc_cloud_id
  folder_id = var.yc_folder_id
  zone      = var.yc_zone
}

resource "yandex_vpc_network" "net" {
  name = "crud-network"
}

resource "yandex_vpc_subnet" "subnet" {
  name           = "crud-subnet"
  zone           = var.yc_zone
  network_id     = yandex_vpc_network.net.id
  v4_cidr_blocks = ["10.0.0.0/24"]
}

resource "yandex_mdb_postgresql_cluster" "pg" {
  name                = "crud-pg"
  environment         = "PRODUCTION"
  network_id          = yandex_vpc_network.net.id
  subnet_id           = yandex_vpc_subnet.subnet.id
  version             = "15"
  resources {
    resource_preset_id = "s2.micro"
    disk_size          = 10
    disk_type_id       = "network-ssd"
  }
  user_name           = var.pg_user
  password            = var.pg_password
  database_name       = var.pg_db
}

resource "yandex_storage_bucket" "minio" {
  name = var.minio_bucket
}

resource "yandex_alb_load_balancer" "lb" {
  name = "crud-lb"
  network_id = yandex_vpc_network.net.id
  // target group, listener, etc. will be defined below
}

resource "yandex_function" "file_handler" {
  name        = "file-handler"
  runtime     = "python38"
  entrypoint  = "handler.main"
  memory      = 128
  execution_timeout = "5s"
  // source code will be placed in a zip archive
}
```
### 6.2 `variables.tf`
```hcl
variable "yc_token" {}
variable "yc_cloud_id" {}
variable "yc_folder_id" {}
variable "yc_zone" { default = "ru-central1-a" }
variable "pg_user" {}
variable "pg_password" {}
variable "pg_db" {}
variable "minio_bucket" { default = "uploads" }
```
### 6.3 `outputs.tf`
```hcl
output "lb_address" {
  value = yandex_alb_load_balancer.lb.listener[0].external_address_spec[0].address
}
```

## 7️⃣ CI/CD (GitHub Actions) (`.github/workflows/ci.yml`)
```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PASS }}
      - name: Build and push app image
        run: |
          docker build -t ${{ secrets.DOCKER_USER }}/crud-app:latest .
          docker push ${{ secrets.DOCKER_USER }}/crud-app:latest
      - name: Terraform Init & Apply
        env:
          YANDEX_CLOUD_TOKEN: ${{ secrets.YC_TOKEN }}
        run: |
          cd infra
          terraform init
          terraform apply -auto-approve
```

## 8️⃣ Тестирование (`tests/`)
* `test_models.py` – проверка создания модели, уникальности `name`.
* `test_routes.py` – запросы к API через `FlaskClient`.
* `test_minio.py` – мокировать `boto3` клиент, проверять, что `upload_file` вызывается.

## 9️⃣ Документация (`README.md`)
* Добавить раздел **Локальный запуск** (docker‑compose up).
* Добавить **API Reference** с примерами `curl`.
* Вставить **Mermaid‑диаграмму** архитектуры (см. ниже).

## 🔟 Мониторинг и логирование
* В Terraform добавить `yandex_monitoring_dashboard` и `yandex_logging_group` для PostgreSQL, MinIO и контейнеров.
* В Flask добавить эндпоинт `/health` returning `{"status":"ok"}`.

---

### Mermaid‑диаграмма архитектуры
```mermaid
graph LR
    subgraph Local
        A[Flask app] --> B[PostgreSQL]
        A --> C[MinIO]
        A --> D[Nginx LB]
    end
    subgraph Cloud
        E[Yandex VPC] --> F[Managed PostgreSQL]
        E --> G[Object Storage]
        E --> H[ALB (Load Balancer)]
        H --> I[Container (Flask)]
        G --> J[Cloud Function (file processing)]
    end
```

---

**Готово.** При необходимости можно сразу перейти к реализации первого файла (`app/config.py`).

