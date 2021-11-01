# easy-auth

## Проект еще на этапе доработки
 
# Запуск в докере
```bash
docker-compose up -d
 ```
 
 
```bash
uvicorn server:app --reload
```

Переменные окружения

SECRET_KEY - Соль для подписания кукисов, чтобы сгенировать свою соль используйте команду
```bash
openssl rand -hex 32
```
