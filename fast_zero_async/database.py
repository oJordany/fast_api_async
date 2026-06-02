from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero_async.settings import Settings

engine = create_engine(Settings().DATABASE_URL)
session = Session(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
