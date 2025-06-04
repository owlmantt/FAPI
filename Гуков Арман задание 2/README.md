

```bash
uvicorn main:app --reload
```

## API Endpoints

- POST `/register` - Регистрация нового пользователя
- POST `/token` - Вход в систему (получение токена)
- GET `/users/me` - Получение информации о текущем пользователе

## Тестирование в Postman

1. Регистрация нового пользователя:
```
POST http://localhost:8000/register
Content-Type: application/json

{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123"
}
```

2. Вход в систему:
```
POST http://localhost:8000/token
Content-Type: application/x-www-form-urlencoded

username=testuser&password=password123
```

3. Получение информации о пользователе:
```
GET http://localhost:8000/users/me
Authorization: Bearer {token}
``` 