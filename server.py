from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

with open('templates/index.html') as file:
    html = file.read()

@app.get('/')
def index_page():
    return Response(html, media_type='text/html')
