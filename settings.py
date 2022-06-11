"""Settings vars define here."""
from urllib.parse import quote_plus

from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env('SECRET_KEY')

PASSWORD_SALT = env('PASSWORD_SALT')

db_username = quote_plus(env('db_username', 'postgres'))
db_password = quote_plus(env('db_password', 'secret'))
db_host_server = env('db_host_server', 'localhost')
db_server_port = quote_plus(env('db_server_port', '5432'))
db_name = env('db_name', 'fastapi')
ssl_mode = quote_plus(env('ssl_mode', 'prefer'))
DATABASE_URL = 'postgresql://{username}:{password}@{host}:{port}/{db_name}?sslmode={ssl_mode}'.format(
    username=db_username,
    password=db_password,
    host=db_host_server,
    port=db_server_port,
    db_name=db_name,
    ssl_mode=ssl_mode,
)
