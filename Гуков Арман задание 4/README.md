# FastAPI JWT Authentication Example

Этот проект демонстрирует реализацию JWT аутентификации с использованием FastAPI.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите сервер:
```bash
uvicorn main:app --reload
```

## API Endpoints

### 1. Регистрация пользователя
- **URL**: `/register`
- **Метод**: POST
- **Тело запроса**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

### 2. Получение токена
- **URL**: `/token`
- **Метод**: POST
- **Form Data**:
  - username: your_username
  - password: your_password

### 3. Получение информации о текущем пользователе
- **URL**: `/users/me`
- **Метод**: GET
- **Заголовки**: 
  - Authorization: Bearer your_token

## Тестирование в Postman

1. Зарегистрируйте нового пользователя через `/register`
2. Получите токен через `/token`
3. Используйте токен для доступа к `/users/me`

## Безопасность

В продакшене необходимо:
1. Изменить SECRET_KEY в security.py
2. Использовать безопасное хранилище для базы данных
3. Настроить CORS и другие меры безопасности 