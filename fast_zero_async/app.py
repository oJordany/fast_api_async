from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero_async.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, world!'}


@app.get('/hello.html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def hello_html():
    return """
    <html>
        <head>
            <title>Hello HTML</title>
        </head>
        <body>
            <h1>Hello HTML</h1>
        </body>
    </html>
    """
