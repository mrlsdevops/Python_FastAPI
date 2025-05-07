from sqlalchemy import create_engine
import os

PASS = os.getenv('DB_PASS')
url = f'postgresql+psycopg://postgres:{PASS}@localhost/fastapi'
print(url)
