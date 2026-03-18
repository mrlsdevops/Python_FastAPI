from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Reference - to establish DB connection
# def get_db():
#     try:
#         conn = psycopg.connect(
#             host='localhost',
#             dbname='fastapi',
#             user='postgres',
#             password=os.getenv('DB_PASS')
#         )
#         return conn
#     except Exception as error:
#         print("DB connection error:", error)
#         raise HTTPException(status_code=500, detail="Database connection error")
