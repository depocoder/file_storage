"""Fast api main app."""
import base64
import hashlib
import hmac
import json
from typing import Optional

from fastapi import Cookie, FastAPI, Form
from fastapi.responses import Response

from settings import PASSWORD_SALT, SECRET_KEY

app = FastAPI()

users = {
    'ivan@ya.ru': {
        'name': 'Ivan',
        'password': '1dcbc1c226e70ce7a71238787d7f70fdf906934dde11d9b662502a8bd8784926',
    },
    'pertr@ya.ru': {
        'name': 'pert',
        'password': '5dff562e6b11e6f23209a2d0054922074cae26e5a98ffef70c6baaf8892bea72',
    },
}


def get_username_from_cookie(username_cookie: str) -> str:
    """Get username from signed cookie."""
    username, sign = username_cookie.split('.')
    username = base64.b64decode(username.encode()).decode()
    valid_sing = hash_sign_cookie(username)
    if hmac.compare_digest(valid_sing, sign):
        return username


def verify_password(username: str, password: str) -> bool:
    user = users.get(username)
    hashed_password = hashlib.sha256(f'{password} + {PASSWORD_SALT}'.encode())
    stored_password_hashed: str = user['password']
    return hashed_password.hexdigest().lower() == stored_password_hashed.lower()


def hash_sign_cookie(cookie: str) -> str:
    """Sign data."""
    return hmac.new(
        SECRET_KEY.encode(), msg=cookie.encode(), digestmod=hashlib.sha256,
    ).hexdigest().upper()


@app.get('/')
def index_page(username: Optional[str] = Cookie(default=None)):
    with open('templates/index.html') as index_file:
        html = index_file.read()
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
            f'You have already logged in your account. Your login {valid_username}',
            media_type='text/html',
        )
    response.delete_cookie('username')
    return response


@app.post('/login')
def process_login_page(username: str = Form(...), password: str = Form(...)):

    if username not in users or not verify_password(username, password):
        incorrect_password_response = {
            'success': False,
            'message': 'Incorrect password or username',
        }
        return Response(
            json.dumps(incorrect_password_response), media_type='application/json',
        )
    login_succes_response = {
        'success': True,
        'message': 'Login success',
    }
    response = Response(
        json.dumps(login_succes_response), media_type='application/json',
    )
    base64_username = base64.b64encode(username.encode()).decode()
    hashed_cookie = hash_sign_cookie(username)
    cookie_value = f'{base64_username}.{hashed_cookie}'
    response.set_cookie(key='username', value=cookie_value)
    return response
