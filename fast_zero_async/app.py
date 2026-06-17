import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI

from fast_zero_async.routers import auth, todos, users
from fast_zero_async.schemas import (
    Message,
)

if sys.platform == 'win32':  # pragma no cover
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )  # pragma no cover
app = FastAPI(title='API FastAPI Async')

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, world!'}


# @app.get('/hello.html',
#   status_code=HTTPStatus.OK,
#   response_class=HTMLResponse
#   )
# def hello_html():
#     return """
#     <html>
#         <head>
#             <title>Hello HTML</title>
#         </head>
#         <body>
#             <h1>Hello HTML</h1>
#         </body>
#     </html>
#     """
