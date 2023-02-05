from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Union, Optional

from app.models import User, Post, Like, Dislike


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserLogin(UserCreate):
    ...


class UserModel(UserCreate):
    id: int
    disabled: bool
    password_hash: str
    posts: List[Post] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    ...


class PostUpdate(PostBase):
    ...


class PostModel(PostBase):
    id: int

    class Config:
        orm_mode = True    


class TokenData(BaseModel):
    email: str | None = None




