import pytest
from app.models import Model
from db.sessions import get_session


@pytest.fixture
def drop_tables(session):
    session.commit()
    Model.metadata.drop_all(session.bind)
    Model.metadata.create_all(session.bind)
    yield


@pytest.fixture(scope='session')
def session():
    yield from get_session()
