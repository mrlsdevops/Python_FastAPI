from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_database

router = APIRouter(
       prefix="/posts",
       tags=['Posts']
)
# # Read all posts
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_database), user_id: int = Depends(oauth2.get_current_user)):
            posts = db.query(models.Post).all()
            return posts 

# Create Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_database), 
                user_id: int = Depends(oauth2.get_current_user)):
    
    print(user_id)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # return{"data": new_post} # That means Fast API is trying to serialize a SQLAlchemy model dirctly 
    # But, here response model expects a pydantic model.
    return new_post # SQLAlchemy model

# # Read latest post
# @router.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"details": post}

# Read post with specific id
@router.get("/{id}", response_model=schemas.Post)
def get_post(id : int, db: Session = Depends(get_database),
             user_id: int = Depends(oauth2.get_current_user)):
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} was not found")
        return post


# Deleting Post
@router.delete("/{id}" , status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_database), 
                user_id: int = Depends(oauth2.get_current_user)):
        print(user_id)
        post = db.query(models.Post).filter(models.Post.id == id)
        if post.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} does not exist")
        post.delete(synchronize_session=False)
        db.commit()

        return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_database),
                user_id: int = Depends(oauth2.get_current_user)):
        print(user_id)
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()

        if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} does not exist")
        
        post_query.update(updated_post.dict(),synchronize_session=False)
        db.commit()

        return post_query.first()