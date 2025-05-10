from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg
from psycopg.rows import dict_row
import os
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_database

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
        
@app.get("/")
def root():
    return {"message": "Welcome to api"}


# # Read all posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_database)):
            posts = db.query(models.Post).all()
            return {"data": posts}

# Create Post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_database)):
        new_post = models.Post(**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return{"data": new_post}
        

# Read latest post
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"details": post}

# Read post with specific id
@app.get("/posts/{id}")
def get_post(id : int, db: Session = Depends(get_database)):
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} was not found")
        return {"post_detail": post}


# Deleting Post
@app.delete("/posts/{id}" , status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_database)):
        post = db.query(models.Post).filter(models.Post.id == id)
        if post.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} does not exist")
        post.delete(synchronize_session=False)
        db.commit()

        return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_database)):
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()

        if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} does not exist")
        
        post_query.update(updated_post.dict(),synchronize_session=False)
        db.commit()

        return {'message': post_query.first()}
