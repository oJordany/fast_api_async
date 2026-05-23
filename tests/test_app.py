from http import HTTPStatus

from fast_zero_async.schemas import UserSchema


def test_root_deve_retornar_ola_mundo(client):
    """
    Esse teste tem 3 etapas (AAA):
    - A: Arrange    - Arranjo
    - A: Act        - Execute a coisa (o SUT)
    - A: Assert     - Garanta que A é A
    """
    # Arrange

    # Act
    response = client.get('/')

    # Assert
    assert response.json() == {'message': 'Hello, world!'}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        '/users',
        json=UserSchema(
            username='alice', email='alice@example.com', password='secret'
        ).model_dump(),
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'alice',
                'email': 'alice@example.com',
            }
        ]
    }


def test_read_user(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_user_not_found(client):
    response = client.get('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json().get('detail') == 'User with id 2 not found'


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'alice',
            'email': 'alice@example.com.br',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com.br',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'alice',
            'email': 'ali@example.com.br',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json().get('detail') == 'User with id 2 not found'


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com.br',
        'id': 1,
    }


def test_delete_user_not_found(client):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json().get('detail') == 'User with id 2 not found'


# def test_hello_html_can_return_html():
#     client = TestClient(app)
#     response = client.get('/hello.html')
#     assert response.headers.get('content-type') == "text/html; charset=utf-8"
#     assert response.status_code == HTTPStatus.OK
