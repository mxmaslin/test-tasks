from fastapi import Depends
from sqlalchemy.orm import Session

from app.models import User, Post, Like, Dislike
from app.auth import get_password_hash
from app.dependencies import get_db


def get_user(db: Session, email: str) -> User:
    return db.query(User).filter(User.email==email).first()


def create_user(db: Session, email: str, password_hash: str):
    user = User(email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


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


def delete_like(db: Session, post_id: int, user: User):
    db.query(Like).delete().where(Dislike.post.id==post_id, Dislike.user==user)


def delete_dislike(db: Session, post_id: int, user: User):
    db.query(Dislike).delete().where(
        Dislike.post.id==post_id, Dislike.user==user
    )

def create_like(db: Session, post_id: int, user: User):
    db.query(Like).insert().values({'post': post_id, 'user': user})


def create_dislike(db: Session, post_id: int, user: User):
    db.query(Dislike).insert().values({'post': post_id, 'user': user})
