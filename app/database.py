from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

PASS = os.getenv('DB_PASS')
if not PASS:
    raise RuntimeError("DB_PASS environment variable not set!")

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://postgres:{PASS}@127.0.0.1/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

