from http import HTTPStatus

import jwt

from fast_zero_async.security import create_access_token


def test_jwt(settings):
    data = {'test': 'test'}

    token = create_access_token(data)

    decoded = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials.'}


def test_jwt_invalid_subject_email(client):
    payload = {
        'sub': '',
    }

    token = create_access_token(data=payload)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials.'}


def test_jwt_invalid_user_db(client):
    payload = {
        'sub': 'batatinhas@example.com',
    }
    token = create_access_token(data=payload)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials.'}
