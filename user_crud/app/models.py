from sqlalchemy import create_engine, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from app.settings import settings


engine = create_engine(settings().SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    password_hash: Mapped[str] = mapped_column(String)

    posts = relationship('Post', backref='user')


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))


class Like(Base):
    __tablename__ = 'likes'
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id'), primary_key=True
    )
    # user: Mapped[User] = relationship(backref='user_likes')
    # post: Mapped[Post] = relationship(backref='post_likes')


class Dislike(Base):
    __tablename__ = 'dislikes'
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id'), primary_key=True
    )
    # user: Mapped[User] = relationship(backref='user_dislikes')
    # post: Mapped[Post] = relationship(backref='post_dislikes')
