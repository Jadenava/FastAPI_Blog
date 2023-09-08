from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags= ["Authenication"]
)

@router.post("/login", response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials! Please try again.")
    
    if not utils.verify(user_credentials.password, user.password): #LAST SPOT I LEFT OFF
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= "Invalid credentials! Please try again.")
    
    access_token = oauth2.create_access_token(data={"user_id": str(user.id)}) # Can't get this line of code to work 7:09

    return {"access_token": access_token, "token_type": "bearer"}