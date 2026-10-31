from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:@Abhi1234@localhost/posta"
SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=settings.database,
)
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:@Abhi1234@localhost/posta"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="posta",
#             user="postgres",
#             password="@Abhi1234",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("database connection is sucessfully")
#         break

#     except Exception as error:
#         print("Connecting to database is failed")
#         print("error : ", error)
#         time.sleep(2)
