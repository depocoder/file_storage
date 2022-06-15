# file_storage


[![Maintainability](https://api.codeclimate.com/v1/badges/7364174229c0f6805dd8/maintainability)](https://codeclimate.com/github/depocoder/file_storage/maintainability)
[![linter check](https://github.com/Corrosion667/quiz-bot/actions/workflows/linter-check.yml/badge.svg)](https://github.com/depocoder/file_storage/actions/workflows/linter-check.yml)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)


## Проект еще на этапе доработки

# Сборка образа

*Сборка образа не обязательна, образ уже есть на dockerhub*

```bash
 docker build -t tifipy/file_storage:master .
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
 
