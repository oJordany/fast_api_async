from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

from fast_zero_async.app import app
from fast_zero_async.database import get_session
from fast_zero_async.models import User, table_registry
from fast_zero_async.security import get_password_hash
from fast_zero_async.settings import Settings


@pytest.fixture
def client(session):
    def get_session_overrides():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_overrides
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(
    *,
    model=User,
    created_time=datetime(2026, 5, 31),
    updated_time=datetime(2026, 6, 1),
):

    def create_fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = created_time
            target.updated_at = created_time

    def update_fake_time_hook(mapper, connection, target):
        if hasattr(target, 'updated_at'):
            target.updated_at = updated_time

    event.listen(User, 'before_insert', create_fake_time_hook)
    event.listen(User, 'before_update', update_fake_time_hook)

    yield created_time, updated_time

    event.remove(User, 'before_insert', create_fake_time_hook)
    event.remove(User, 'before_update', update_fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: Session):
    password = 'testtest'
    user = User(
        username='Test',
        email='teste@test.com',
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )

    return response.json()['access_token']


@pytest.fixture
def settings():
    settings = Settings()
    return settings
