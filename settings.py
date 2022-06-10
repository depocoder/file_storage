from environs import Env

env = Env()

SECRET_KEY = env('SECRET_KEY')

PASSWORD_SALT = env('PASSWORD_SALT')
