from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint

from FastAPI90 import models


class UserResponse(BaseModel):
    email:EmailStr
    id:int
    created_at:datetime
    class Config:  # because we need to convert the SQLachemy model to a regual pydantic model
        from_attributes = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str



class PostBase(BaseModel):
    title: str  # expects a String title
    content: str  # expects a String Content
    published: bool = True # Publish is optional defaults to True


class Post(PostBase):
    id:int
    created_at:datetime
    owner_id : int
    owner : UserResponse
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str  # expects a String title
    content: str  # expects a String Content
    published: bool = True  # Publish is optional defaults to True

class PostUpdate(BaseModel):
    title: str  # expects a String title
    content: str  # expects a String Content
    published: bool = True  # Publish is optional defaults to True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None #None default argument

class Votes(BaseModel):
    post_id:int
    dir:conint(le = 1,gt=-1)

#ResponseSchemas

class PostResponse(PostBase):
    id : int
    created_at : datetime
    owner_id:int
    owner:UserResponse

class PostOut(BaseModel):
    post: PostResponse
    votes : int

    class Config:#because we need to convert the SQLachemy model to a dictionar
        from_attributes = True












