from pydantic import BaseModel


class UserLoginModel(BaseModel):
    email: str
    password: str


class UserSignupModel(BaseModel):
    email: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
