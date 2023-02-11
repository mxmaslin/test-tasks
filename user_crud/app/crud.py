from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate, UserDelete, UserGet


def get_user(db: Session, data: UserGet) -> User:
    return db.query(User).filter(User.phone_number==data.phone_number).first()


def create_user(db: Session, data: UserCreate):
    user = User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, data: UserDelete):
    user = get_user(db, data)
    db.delete(user)
    db.commit()
