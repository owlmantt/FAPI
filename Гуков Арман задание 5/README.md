# FastAPI JWT Authentication с ролями пользователей

Этот проект демонстрирует реализацию JWT аутентификации с ролями пользователей, используя FastAPI.

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
- **Примечание**: При регистрации автоматически назначается роль "user"

### 2. Получение токена
- **URL**: `/token`
- **Метод**: POST
- **Form Data**:
  - username: your_username
  - password: your_password

### 3. Информация о текущем пользователе
- **URL**: `/users/me`
- **Метод**: GET
- **Заголовки**: 
  - Authorization: Bearer your_token

### 4. Список всех пользователей (только для админов)
- **URL**: `/admin/users`
- **Метод**: GET
- **Заголовки**: 
  - Authorization: Bearer your_token
- **Требуется роль**: admin

## Тестирование в Postman

1. Зарегистрируйте нового пользователя через `/register`
2. Получите токен через `/token`
3. Попробуйте получить доступ к `/admin/users` (должно быть отказано с кодом 403)
4. Измените роль пользователя на "admin" в базе данных
5. Снова попробуйте получить доступ к `/admin/users` (должно быть разрешено)

## Изменение роли пользователя

Для изменения роли пользователя на "admin", используйте SQLite клиент:

```sql
UPDATE users SET role = 'admin' WHERE username = 'your_username';
```

## Безопасность

В продакшене необходимо:
1. Изменить SECRET_KEY в security.py
2. Использовать безопасное хранилище для базы данных
3. Настроить CORS и другие меры безопасности 