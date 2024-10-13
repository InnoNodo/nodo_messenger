from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .entities import Base

def initialize_database(engine):
    with engine.begin() as conn:
        Base.metadata.create_all(conn)

def get_session_maker(connection_string):
    engine = create_engine(connection_string)
    session_maker = sessionmaker(bind=engine, expire_on_commit=False)

    initialize_database(engine)

    return session_maker
