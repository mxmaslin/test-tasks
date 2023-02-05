from fastapi import Depends
from sqlalchemy.orm import Session

from app.models import User, Post
from app.auth import get_password_hash


def get_user(db: Session, email) -> User:
    return db.query(User).filter(User.email==email).first()


def create_user(db: Session, email: str, password_hash: str):
    return db.query(User).insert().values(
        {'email': email, 'password_hash': password_hash}
    )


def get_post(db: Session, post_id: int) -> Post:
    return db.query(Post).filter(Post.id==post_id).first()


def get_user_post(db: Session, post_id: int):
    return db.query(User).join(User.posts).filter(Post.id==post_id).all()


def get_posts(db: Session, limit: int = 0, offset: int = 0):
    return db.query(Post).filter().limit(limit).offset(offset)


def create_post(db: Session, title: str, content: str):
    return db.query(Post).insert().values(
        {'title': title, 'content': content}
    )


def update_post(db: Session, post_id: int, title: str, content: str):
    return db.query(Post).update().where(Post.id==post_id).values(
        {'title': title, 'content': content}
    )


def delete_post(db: Session, post_id: int):
    db.query(Post).delete().where(Post.id==post_id)
