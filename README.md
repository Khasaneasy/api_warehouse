# Api_Warehouse
Api_Warehouse - это REST API для управления заказами и товарами.


## Стек Технологий
- Python 3.9+
- FastAPI
- SQLAlchemy
- Asyncpg (PostgreSQL driver)
- Uvicorn
- pydantic-settings
- Fast-API


## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone git@github.com:Khasaneasy/api_warehouse.git
cd warehouse-api
```

### 2. Создать и активировать виртуальное окружение

python -m venv venv
source venv/bin/activate (Linux/MacOS)
venv\Scripts\activate (Windows)


### 3. Создание файла конфигурации .env

DB_HOST=localhost
DB_PORT=5432
DB_NAME=warehouse_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password


### 4. Применение миграций и Запуск сервера

python -m app.database.create_tables

uvicorn app.main:app --reload

### 5. Эндпоинты API
После запуска сервера вы сможете получить доступ к API по адресу http://127.0.0.1:8000

Эндпоинты для товаров:
POST /products — Создание нового товара.
GET /products — Получение списка всех товаров.
GET /products/{id} — Получение информации о товаре по ID.
PUT /products/{id} — Обновление информации о товаре.
DELETE /products/{id} — Удаление товара.
Эндпоинты для заказов:
POST /orders — Создание нового заказа с проверкой наличия товара.
GET /orders — Получение списка всех заказов.
GET /orders/{id} — Получение информации о заказе по ID.
PATCH /orders/{id}/status — Обновление статуса заказаю

Автор:

>https://github.com/Khasaneasy