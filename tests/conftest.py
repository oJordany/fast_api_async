import pytest
from starlette.testclient import TestClient

from fast_zero_async.app import app


@pytest.fixture
def client():
    return TestClient(app)
