from sqlalchemy.orm import Session

from models import User, Post, Like, Dislike
from schemas import PostModel


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
    return db.query(Post).join(
        User,
        User.id == Post.user_id
    ).filter(Post.id==post_id).first()


def get_posts(db: Session, limit: int = 0, offset: int = 0):
    return db.query(Post).filter().limit(limit).offset(offset)


def create_post(db: Session, user_id: int, title: str, content: str):
    post = Post(user_id=user_id, title=title, content=content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(
    db: Session,
    post: Post,
    post_new_data: PostModel
):
    new_data = post_new_data.dict(exclude_unset=True)
    for k, v in new_data.items():
        setattr(post, k, v)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: int):
    post = get_post(db, post_id)
    db.delete(post)
    db.commit()


def delete_like(db: Session, post_id: int, user_id: int):
    like = db.query(Like).filter(
        Like.post_id==post_id, Like.user_id==user_id
    ).first()
    if like is not None:
        db.delete(like)
        db.commit()


def delete_dislike(db: Session, post_id: int, user_id: int):
    dislike = db.query(Dislike).filter(
        Dislike.post_id==post_id, Dislike.user_id==user_id
    ).first()
    if dislike is not None:
        db.delete(dislike)
        db.commit()


def create_like(db: Session, post_id: int, user_id: int):
    like = Like(post_id=post_id, user_id=user_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like


def create_dislike(db: Session, post_id: int, user_id: int):
    dislike = Dislike(post_id=post_id, user_id=user_id)
    db.add(dislike)
    db.commit()
    db.refresh(dislike)
    return dislike
