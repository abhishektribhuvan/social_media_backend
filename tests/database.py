from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL, make_url
from app.config import settings
import os
from app.database import get_db

from app.database import Base
import pytest

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:@Abhi1234@localhost/posta"

render_url = os.getenv("DATABASE_URL")

if render_url:
    SQLALCHEMY_DATABASE_URL = make_url(render_url).set(drivername="postgresql+ psycopg")
else:
    SQLALCHEMY_DATABASE_URL = URL.create(
        drivername="postgresql+psycopg",
        username=settings.database_username,
        password=settings.database_password,
        host=settings.database_hostname,
        port=settings.database_port,
        database="backend_testing_db",
    )

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:@Abhi1234@localhost/posta"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)
testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base = declarative_base()


# Dependency
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testing_session()
    try:
        yield db
    finally:
        db.close()


# we are making this becoz we wann do multiply
# testing so we are droping the initital db and then creating all agin to test new
@pytest.fixture()
def client(session):
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = overrid_get_db

    return TestClient(app)


# for testing we override the original db
#  and use the other testing db here
# this will overide the get_db by this overide_get_db
