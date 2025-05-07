from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import os
import time 
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_database

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# @app.on_event("startup")
# def startup():
#     models.Base.metadata.create_all(bind=engine)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None



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
        
@app.get("/")
def root():
    return {"message": "Welcome to api"}

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_database)):
#     return {"status": "Success"}

@app.get("/sqlalchemy")
def test_connection(db: Session = Depends(get_database)):
    db.execute("SELECT 1")
    return {"status": "ok"}

# # Read all posts
@app.get("/posts")
def get_posts():
    conn = get_db()
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM posts")
            posts = cur.fetchall()
            return {"data": posts}
    finally:
        conn.close()

# Create Post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    conn = get_db()
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""INSERT INTO posts (title, content, published)
                        VALUES (%s, %s, %s) RETURNING * """,
                        (post.title, post.content, post.published))
            new_post = cur.fetchone()
            # commit changes to postgresql
            conn.commit()

            return{"data": new_post}
    finally:
        conn.close()
        

# Read latest post
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"details": post}

# Read post with specific id
@app.get("/posts/{id}")
def get_post(id : int):
    conn = get_db()
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
            posts = cur.fetchone()
            if not posts:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"post with id: {id} was not found")
            return {"data": posts}      
    finally:
        conn.close()


# Deleting Post
@app.delete("/posts/{id}" , status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    conn = get_db()
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
            deleted_post = cur.fetchone()
            conn.commit()

            if deleted_post == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"post with id: {id} does not exist")
            return Response(status_code = status.HTTP_204_NO_CONTENT)
    finally:
        conn.close()

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    conn = get_db()
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
            RETURNING *""",
                    (post.title, post.content, post.published, str(id),))
            updated_post = cur.fetchone()
            conn.commit()
            if updated_post == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
            return {'message': updated_post}
    finally:
        conn.close()
