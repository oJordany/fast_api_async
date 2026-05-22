from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero_async.app import app


def test_root_deve_retornar_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA):
    - A: Arrange    - Arranjo
    - A: Act        - Execute a coisa (o SUT)
    - A: Assert     - Garanta que A é A
    """
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get('/')

    # Assert
    assert response.json() == {'message': 'Hello, world!'}
    assert response.status_code == HTTPStatus.OK


def test_hello_html_can_return_html():
    client = TestClient(app)
    response = client.get('/hello.html')
    assert response.headers.get('content-type') == "text/html; charset=utf-8"
    assert response.status_code == HTTPStatus.OK
