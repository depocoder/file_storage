from fastapi import FastAPI, Form
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
def index_page():
    with open('templates/index.html') as file:
        html = file.read()
    return Response(html, media_type='text/html')

@app.post('/login')
def process_login_page(username : str = Form(...), password: str = Form(...)):
    user = users.get(username)
    if not user or user['password'] != password:
        return Response(
            f'Incorrect password or username', media_type='text/html'
        )
    password = user.get('password')
    return Response(
        f'your login {username}, your balance is {user["balance"]}', media_type='text/html'
        )
