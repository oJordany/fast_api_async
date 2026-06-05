from http import HTTPStatus

from fast_zero_async.schemas import UserPublic, UserSchema


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


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users',
        headers={
            'Authorization': f'Bearer {token}',
        },
    )
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


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'alice',
            'email': 'alice@example.com.br',
            'password': 'secret',
        },
        headers={
            'Authorization': f'Bearer {token}',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com.br',
        'id': 1,
    }


def test_update_not_enough_permissions(client, user, token):
    response = client.put(
        '/users/2',
        json={
            'username': 'alice',
            'email': 'ali@example.com.br',
            'password': 'secret',
        },
        headers={
            'Authorization': f'Bearer {token}',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json().get('detail') == 'Not enough permissions'


def test_update_integrity_error(client, user, token):
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
        headers={
            'Authorization': f'Bearer {token}',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Username or Email already exists.',
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={
            'Authorization': f'Bearer {token}',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_enough_permissions(client, user, token):
    response = client.delete(
        '/users/2',
        headers={
            'Authorization': f'Bearer {token}',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json().get('detail') == 'Not enough permissions'
