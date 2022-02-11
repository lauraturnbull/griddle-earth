from contextlib import contextmanager

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from engine.adapters.api.app import AppConfig, create_app
from engine.adapters.postgres.model import Base

eng = create_engine("postgresql:///griddle-earth")
Session = sessionmaker(bind=eng)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


@pytest.fixture()
def engine() -> Engine:
    yield eng
    eng.dispose()
    with session_scope() as conn:
        for table in Base.metadata.sorted_tables:
            conn.execute(f"TRUNCATE {table.name} RESTART IDENTITY CASCADE;")


def create_test_app(
    engine: Engine,
) -> FastAPI:
    mock_config = AppConfig(
        DB_URL=str(engine.url),
    )
    return create_app(mock_config)


@pytest.fixture
def app(engine):
    yield create_test_app(engine)


@pytest.fixture
def client(app: FastAPI):
    yield TestClient(app, raise_server_exceptions=True)
