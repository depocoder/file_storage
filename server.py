from typing import Optional
import hmac
import hashlib
import base64

from fastapi import FastAPI, Form, Cookie
from fastapi.responses import Response

from settings import SECRET_KEY

app = FastAPI()


users = {
    'ivan@ya.ru': {
        'name': 'Ivan',
        'password': 'qweqweqweqwe',
        'balance': 100_000
    },    
    'pertr@ya.ru': {
        'name': 'pert',
        'password': 'qweqweqweqwe2',
        'balance': 0
    }
}


def get_username_from_cookie(username_cookie: str) -> Optional[str]:
    '''Получение username'a из подписанной куки'''
    username, sign = username_cookie.split('.')
    username = base64.b64decode(username.encode()).decode()
    valid_sing = hash_sign_cookie(username)
    if hmac.compare_digest(valid_sing, sign):
        return username


def hash_sign_cookie(cookie: str) -> str:
    '''Возвращает подписанные данные'''
    return hmac.new(
            SECRET_KEY.encode(), msg=cookie.encode(), digestmod=hashlib.sha256
        ).hexdigest().upper()
    

@app.get('/')
def index_page(username: Optional[str] = Cookie(default=None)):
    with open('templates/index.html') as file:
        html = file.read()
        response = Response(html, media_type='text/html')
    if not username:
        return response

    valid_username = get_username_from_cookie(username)
    if not valid_username:
        response.delete_cookie('username')
        return response

    user = users.get(valid_username)
    if user:
        return Response(
            f'You have alredy logged in your account. Your login {valid_username}, your balance is {user["balance"]}', media_type='text/html'
            )
    else:
        response.delete_cookie('username')
        return response


@app.post('/login')
def process_login_page(username : str = Form(...), password: str = Form(...)):
    user = users.get(username)
    if not user or user['password'] != password:
        return Response(
            f'Incorrect password or username', media_type='text/html'
        )
    password = user.get('password')
    response = Response(
        f'your login {username}, your balance is {user["balance"]}', media_type='text/html'
        )
    base64_username = base64.b64encode(username.encode()).decode()
    hashed_cookie = hash_sign_cookie(username)
    cookie_value = f"{base64_username}.{hashed_cookie}"
    response.set_cookie(key='username', value=cookie_value)
    return response
