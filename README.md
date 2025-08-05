
# User Balance Service

Микросервис для управления балансом пользователей с gRPC и HTTP (FastAPI) интерфейсами.

## 🚀 Запуск проекта

### Требования
- Python 3.12+
- Poetry (для управления зависимостями)
- Docker (опционально)

### Установка
```bash
poetry install
```

### Запуск в разработке
```bash
poetry run uvicorn app.main:app --reload
```

### Запуск с Docker
```bash
docker-compose up --build
```

## 📡 API Интерфейсы

### HTTP (FastAPI)
- Документация: `http://localhost:8000/docs`
- Доступные эндпоинты:
  - `GET /balance/{user_id}` - Получить баланс
  - `POST /transaction` - Создать транзакцию

### gRPC
- Порт: 50051
- Сервис: `BalanceService`
- Методы:
  - `GetBalance` - Получить баланс
  - `CreateTransaction` - Создать транзакцию

## 🛠 Управление базой данных

### Миграции
Создание новой миграции:
```bash
poetry run alembic revision --autogenerate -m "description"
```

Применение миграций:
```bash
poetry run alembic upgrade head
```

### Тестовые данные
```bash
psql -U your_user -d your_db -f test_data.sql
```

## ⚙️ Конфигурация (Environment Variables)

Основные переменные окружения для настройки сервиса:

| Переменная              | Значение по умолчанию                          | Описание                              |
|-------------------------|-----------------------------------------------|---------------------------------------|
| `PROJECT_NAME`          | `User Balance Service`                        | Название сервиса                      |
| `VERSION`               | `1.0.0`                                       | Версия API                            |
| `DESCRIPTION`           | `API для управления пользовательским балансом` | Описание сервиса                      |
| `DATABASE_URL`          | `postgresql+asyncpg://postgres:postgres@db:5432/postgres` | URL подключения к PostgreSQL |
| `AUTH_SERVICE_URL`      | `http://auth-service:8001/validate`          | URL сервиса аутентификации            |
| `AUTH_SERVICE_SECRET`   | `supersecretkey`                              | Секретный ключ для аутентификации     |
| `GRPC_PORT`             | `50051`                                       | Порт для gRPC сервера                 |
| `HTTP_PORT`             | `8000`                                        | Порт для HTTP сервера (FastAPI)       |
| `CELERY_BROKER_URL`     | `redis://redis:6379/0`                        | URL брокера сообщений (Redis)         |

### Пример `.env` файла
```env
PROJECT_NAME=User Balance Service
VERSION=1.0.0
DESCRIPTION=API для управления пользовательским балансом
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres
AUTH_SERVICE_URL=http://auth-service:8001/validate
AUTH_SERVICE_SECRET=supersecretkey
GRPC_PORT=50051
HTTP_PORT=8000
CELERY_BROKER_URL=redis://redis:6379/0
```
## 📦 Зависимости
Основные зависимости:
- FastAPI - HTTP сервер
- SQLAlchemy - ORM
- Alembic - Миграции БД
- gRPC - gRPC сервер
- Celery - Асинхронные задачи

Полный список в `pyproject.toml`
```