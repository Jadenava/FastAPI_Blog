from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db

router=APIRouter(
    prefix="/users",
    tags=["Users"]
    )
 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UsersCreateResponse)
def create_users(user: schemas.UsersCreate, db: Session = Depends(get_db)):
    
    # Hash the password -> user.password
    hased_password = utils.hash(user.password)
    user.password = hased_password

    new_user = models.User(**user.model_dump()) # unpacks post object to dict type so when you scale up attributes you don't need to assign to each like
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/")
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users


@router.get("/{id}", response_model = schemas.UsersCreateResponse)
def get_single_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} can not be found!")

    return user