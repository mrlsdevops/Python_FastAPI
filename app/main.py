from fastapi import FastAPI, HTTPException
import psycopg
from psycopg.rows import dict_row
import os
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        conn = psycopg.connect(
            host='localhost',
            dbname='fastapi',
            user='postgres',
            password=os.getenv('DB_PASS')
        )
        return conn
    except Exception as error:
        print("DB connection error:", error)
        raise HTTPException(status_code=500, detail="Database connection error")



my_posts = [{"title": "title of post1" , "content": "content of post1", "id": 1},
            {"title": "Favourite food", "content": "Potato","id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] ==id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
        
@app.get("/")
def root():
    return {"message": "Welcome to api"}



