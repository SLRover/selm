from app import create_app
import pytest


@pytest.fixture
def client():
    create_app().config['TESTING'] = True

    with create_app().test_client() as client:
        with create_app().app_context():
            create_app()
        yield client


def test_app(client):
    rv = client.get('/')
    assert b'/login' in rv.data
