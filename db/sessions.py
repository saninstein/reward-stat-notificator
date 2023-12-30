from contextlib import contextmanager
from typing import Union

from sqlalchemy.orm import Session, scoped_session

from .connection import SessionLocal

SessionType = Union[Session, scoped_session]
session: Union[Session, scoped_session] = scoped_session(SessionLocal)


def get_session():
    session: SessionType = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


db_session = contextmanager(get_session)
