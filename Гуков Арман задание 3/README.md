# FastAPI JWT Authentication Demo

Этот проект демонстрирует реализацию JWT аутентификации с использованием FastAPI.

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

2. Активируйте виртуальное окружение:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

Запустите сервер с помощью команды:
```bash
uvicorn main:app --reload
```

## API Endpoints

- POST `/register` - Регистрация нового пользователя
- POST `/token` - Получение JWT токена (логин)
- GET `/users/me` - Получение информации о текущем пользователе (требует JWT токен)

## Swagger Documentation

После запуска сервера, документация API доступна по адресу:
http://localhost:8000/docs 