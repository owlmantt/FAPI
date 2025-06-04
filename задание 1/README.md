# Задание 1 - FastAPI User Authentication

Простой API для регистрации и аутентификации пользователей с использованием FastAPI.

## Технологии

- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Pydantic

## Функциональность

- Регистрация новых пользователей (/register)
- Аутентификация пользователей (/login)
- Хранение данных в PostgreSQL

## Установка и запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте PostgreSQL и создайте базу данных:
```sql
CREATE DATABASE users_db;
```

3. Запустите приложение:
```bash
uvicorn main:app --reload
```

## API Endpoints

### POST /register
Регистрация нового пользователя
```json
{
    "username": "test_user",
    "password": "test_password"
}
```

### POST /login
Вход в систему
```json
{
    "username": "test_user",
    "password": "test_password"
}
``` 