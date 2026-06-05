from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'Bearer' in token['token_type']


def test_get_token_for_invalid_username(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'batatinhas@email', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'Incorrect username or password',
    }


def test_get_token_for_invalid_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': '<PASSWORD>'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'Incorrect username or password',
    }
