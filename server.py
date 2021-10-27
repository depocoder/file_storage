from typing import Optional

from fastapi import FastAPI, Form, Cookie
from fastapi.responses import Response


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

@app.get('/')
def index_page(username: Optional[str] = Cookie(default=None)):
    with open('templates/index.html') as file:
        html = file.read()
        response = Response(html, media_type='text/html')

    if not username:
        return response
    user = users.get(username)
    if user:
        return Response(
            f'You have alredy logged in your account. Your login {username}, your balance is {users[username]["balance"]}', media_type='text/html'
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
    response.set_cookie(key='username', value=username)
    return response
