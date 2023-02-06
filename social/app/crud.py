from fastapi import Depends
from sqlalchemy.orm import Session

from app.models import User, Post, Like, Dislike
from app.auth import get_password_hash
from app.dependencies import get_db


def get_user(email, db: Session = Depends(get_db)) -> User:
    return db.query(User).filter(User.email==email).first()


def create_user(email: str, password_hash: str, db: Session = Depends(get_db)):
    return db.query(User).insert().values(
        {'email': email, 'password_hash': password_hash}
    )


def get_post(post_id: int, db: Session = Depends(get_db)) -> Post:
    return db.query(Post).filter(Post.id==post_id).first()


def get_user_post(post_id: int, db: Session = Depends(get_db)):
    return db.query(User).join(User.posts).filter(Post.id==post_id).all()


def get_posts(db: Session = Depends(get_db), limit: int = 0, offset: int = 0):
    return db.query(Post).filter().limit(limit).offset(offset)


def create_post(title: str, content: str, db: Session = Depends(get_db)):
    return db.query(Post).insert().values(
        {'title': title, 'content': content}
    )


def update_post(
    post_id: int, title: str, content: str, db: Session = Depends(get_db)
):
    return db.query(Post).update().where(Post.id==post_id).values(
        {'title': title, 'content': content}
    )


def delete_post(post_id: int, db: Session = Depends(get_db)):
    db.query(Post).delete().where(Post.id==post_id)


def delete_like(post_id: int, user: User, db: Session = Depends(get_db)):
    db.query(Like).delete().where(Dislike.post.id==post_id, Dislike.user==user)


def delete_dislike(post_id: int, user: User, db: Session = Depends(get_db)):
    db.query(Dislike).delete().where(
        Dislike.post.id==post_id, Dislike.user==user
    )

def create_like(post_id: int, user: User, db: Session = Depends(get_db)):
    db.query(Like).insert().values({'post': post_id, 'user': user})


def create_dislike(post_id: int, user: User, db: Session = Depends(get_db)):
    db.query(Dislike).insert().values({'post': post_id, 'user': user})
