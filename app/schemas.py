from pydantic import BaseModel, EmailStr, Field
from pydantic.types import conint
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated


class User(BaseModel):
    username: str
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str 
    published: bool=True

class PostCreate(PostBase):
    user_id: Optional[int] = 0

class PostResponse(PostBase):
    id: int
    # user_id: int
    created_at: datetime
    owner: User

    class Config:
        from_attributes = True

class PostResponse2(BaseModel):
    Post: PostResponse 
    Votes: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class VotesInput(BaseModel):
    # user_id: Optional[int] = 0
    post_id: int
    vote: Annotated[int, Field(le=1)]
