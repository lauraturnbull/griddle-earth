from contextlib import contextmanager
from typing import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker


@contextmanager
def session_scope(session_cls: sessionmaker) -> Iterator[Session]:
    session = session_cls()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def session_cls() -> Iterator[sessionmaker]:
    """This is overridden in engine.adapters.api.app."""
    raise NotImplementedError("Dependency not injected")


def session(
    sess_cls: sessionmaker = Depends(session_cls),
) -> Iterator[Session]:
    with session_scope(sess_cls) as session:
        yield session
