from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fast_zero_async.app import app
from fast_zero_async.models import User, table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
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
