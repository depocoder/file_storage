# file_storage

## Проект еще на этапе доработки

# Сборка образа

*Сборка образа не обязательна, образ уже есть на dockerhub*

```bash
 docker build -t tifipy/easy-auth:master .
```
 
Переменные окружения

`SECRET_KEY` - Соль для подписания кукисов

`PASSWORD_SALT` - Соль для шифрования паролей пользователей

Чтобы получить строку из 32 символов выполните команду в терминале

```bash
openssl rand -hex 32
```

Перед запуском создайте `.env` файл

Пример .env файла 

```
SECRET_KEY=3abd7c12cb7c4c3a94e2b99feee8566d70d8f75884265a341af0ab615f4451c5
PASSWORD_SALT=00c2c11983cb83e7741afa305842a19ad55db660e194aa75f5a0736d171b27fb
```

# Запуск в докере

```bash
docker-compose up -d
 ```
 
