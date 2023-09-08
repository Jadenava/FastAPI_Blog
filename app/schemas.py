from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional



class UsersCreateResponse(BaseModel):
    # exclude sending back the password to user
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    created_at: datetime

    class Config:
        orm_mode = True


class Posts(BaseModel):
    # validation of schema using the below template
    title: str
    content: str
    published: bool = True


class PostUpdate(Posts):
    version_number: int

class PostsResponse(Posts):
    id: int
    created_at: datetime
    user_id: int
    # test: bool = True
    owner: UsersCreateResponse
    
    class Config:
        orm_mode = True

class PostVote(BaseModel):
    Post: PostsResponse
    votes: int

    class Config:
        orm_mode = True

    
class UsersCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    vote_direction: conint(le=1)