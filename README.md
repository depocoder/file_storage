# easy-auth
 
```bash
uvicorn server:app --reload
```

Переменные окружения

SECRET_KEY - Соль для подписания кукисов, чтобы сгенировать свою соль используйте команду
```bash
openssl rand -hex 32
```