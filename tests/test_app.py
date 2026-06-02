from http import HTTPStatus

from fast_zero_async.schemas import UserPublic, UserSchema


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


def test_create_user_with_same_username(client, user):
    response = client.post(
        '/users',
        json={
            'username': user.username,
            'email': 'email@example.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'User with this username already exists.'
    }


def test_create_user_with_same_email(client, user):
    response = client.post(
        '/users',
        json={
            'email': user.email,
            'username': 'NovoUser',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'User with this email already exists.'
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_client(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == UserPublic.model_validate(user).model_dump()


def test_read_user_not_found(client):
    response = client.get('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json().get('detail') == 'User not found'


def test_update_user(client, user):
    response = client.put(
        f'/users/{user.id}',
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


def test_update_user_not_found(client, user):
    response = client.put(
        '/users/2',
        json={
            'username': 'alice',
            'email': 'ali@example.com.br',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json().get('detail') == 'User not found'


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com.br',
            'password': 'secret',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'alice',
            'email': user.email,
            'password': user.password,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Username or Email already exists.',
    }


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client, user):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json().get('detail') == 'User not found'


# def test_hello_html_can_return_html():
#     client = TestClient(app)
#     response = client.get('/hello.html')
#     assert response.headers.get('content-type') == "text/html; charset=utf-8"
#     assert response.status_code == HTTPStatus.OK
