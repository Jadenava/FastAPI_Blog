from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )


# @router.get("/", response_model=List[schemas.PostsResponse]) 
@router.get("/", response_model=List[schemas.PostVote]) # response_model is sending a List of all post in the form of schema
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), threshold: int = 10, search: Optional[str]= ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # (in case you only want the logged in user to fetch all THEIR post only) - posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(threshold).all()
    # posts = db.query(models.Post).all()
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
                models.Post.title.contains(search)).limit(threshold).all()
    
    posts = list ( map (lambda x : x._mapping, posts) )

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.PostsResponse)
def create_posts(post: schemas.Posts, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published)) # To avoid SQL injections in DB by bad actors implement this way
    # created_post = cursor.fetchone() # saves the newly created post into variable and returns the values of the newly created post
    # conn.commit()

   
    new_post = models.Post(user_id = current_user.id, **post.model_dump()) # unpacks post object to dict type so when you scale up attributes you don't need to assign to each like
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model= schemas.PostVote)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # single_post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} can not be found!")

    # Only if I want the logged in user to be able to retrive a post they are the owner of 
    #  if post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not allowed to delete post id: {id} because you are not the owner!")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id: {id} does not exist!")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not allowed to delete post id: {id} because you are not the owner!")

    post_query.delete(synchronize_session = False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}", status_code= status.HTTP_202_ACCEPTED, response_model=schemas.PostsResponse)
def update_post(id: int, post_update: schemas.Posts, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #                (updated_post.title, updated_post.content, updated_post.published, (str(id))))
    # latest_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id: {id} does not exist!")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not allowed to update post id: {id} because you are not the owner!")

    post_query.update(post_update.model_dump(),synchronize_session=False)

    db.commit()
    
    return post_query.first()