from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate


def get_user(db: Session, phone_number: str) -> User:
    return db.query(User).filter(User.phone_number==phone_number).first()


def create_user(db: Session, data: UserCreate):
    user = User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, phone_number: str):
    user = get_user(db, phone_number)
    db.delete(user)
    db.commit()
