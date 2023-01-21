from pydantic import BaseModel


class UserLoginModel(BaseModel):
    email: str
    password: str


class UserSignupModel(BaseModel):
    email: str
    password: str


class PostCreateModel(BaseModel):
    title: str
    content: str


class PostUpdateModel(BaseModel):
    title: str
    content: str


class TokenData(BaseModel):
    email: str | None = None
