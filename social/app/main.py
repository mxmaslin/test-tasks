import sys

from datetime import timedelta
from pathlib import Path

import aiohttp
import uvicorn

from fastapi import Depends, FastAPI, HTTPException, status, Response
from fastapi.responses import JSONResponse
from redis import Redis
from sqlalchemy.orm import Session

app_path = Path.cwd().parent
sys.path.append(str(app_path))

from app import crud
from app.auth import (
    authenticate_user, create_access_token, get_current_active_user,
    get_password_hash
)
from app.dependencies import get_redis, get_db
from app.logger import logger
from app.schemas import (
    PostCreate, PostUpdate, UserLogin, UserCreate, UserModel
)
from app.models import Post, User, Like, Dislike
from app.settings import settings, Settings

app = FastAPI()


@app.post('/token', tags=['auth'])
async def login_for_access_token(
    user_data: UserLogin,
    db: Session = Depends(get_db),
    settings: Settings = Depends(settings)
) -> Response:
    user: User = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        logger.error('Failed to authenticate user')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={'sub': user_data.email}, expires_delta=access_token_expires
    )
    return JSONResponse(
        content={'access_token': access_token, 'token_type': 'bearer'}
    )


@app.post('/signup', tags=['auth'])
async def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    settings: Settings = Depends(settings)
) -> Response:
    # Verify email with emailhunter.co
    async with aiohttp.ClientSession() as session:
        url = settings.EMAILHUNTER_URL.format(
            email=user_data.email,
            api_key=settings.EMAILHUNTER_API_KEY
        )
        async with session.get(url) as response:
            response = await response.json()
            if response.get('result') == 'undeliverable':
                logger.error('Email is undeliverable')
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Invalid email'
                )

    password_hash = get_password_hash(user_data.password)

    try:
        user = crud.create_user(db, user_data.email, password_hash)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error writing user to db'
        )

    return JSONResponse(content={'message': f'User {user.id} created'})


@app.post('/posts', tags=['posts'])
async def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Response:
    try:
        post = crud.create_post(
            db, current_user.id, post_data.title, post_data.content
        )
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error writing post to db'
        )
    return JSONResponse(content={'message': f'Post {post.id} created'})


@app.get('/posts', tags=['posts'])
async def read_posts(
    limit: int = 10, offset: int = 0, db: Session = Depends(get_db)
) -> Response:
    posts = crud.get_posts(db, limit, offset)
    return JSONResponse(
        content={
            'posts': [
                {
                    'id': post.id,
                    'title': post.title,
                    'content': post.content
                } for post in posts
            ]
        }
    )


@app.get('/post/{post_id}', tags=['posts'])
async def read_post(post_id: int, db: Session = Depends(get_db)) -> Response:
    post: Post = crud.get_post(db, post_id)
    if not post:
        logger.error(f'Post {post_id} not found')
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Post does not exist'
        )
    return JSONResponse(
        content={'data': {'title': post.title, 'content': post.content}}
    )


@app.put('/posts/{post_id}', tags=['posts'])
async def update_post(
    post_id: int,
    post_new_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Response:
    try:
        post: Post = crud.get_user_post(db, post_id)
    except Exception as e:
        logger.error(str(e))
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Post does not exist'
        )
    if post.user != current_user:
        message = 'Unable to update other\'s posts'
        logger.error(message)
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    try:
        crud.update_post(db, post, post_new_data)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error writing post update to db'
        )

    return JSONResponse(content={'message': f'Post {post.id} updated'})


@app.delete('/posts/{post_id}', tags=['posts'])
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
):
    post: Post = crud.get_user_post(db, post_id)
    if not post:
        logger.error(f'Post {post_id} not found')
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Post does not exist'
        )

    if post.user != current_user:
        message = 'Unable to delete other\'s posts'
        logger.error(message)
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    try:
        crud.delete_post(db, post.id)
    except Exception as e:
        logger.error(str(e))
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error on post delete'
        )

    return JSONResponse(content={'message': f'Post {post.id} deleted'})


@app.post('/posts/{post_id}/like', tags=['posts'])
async def like_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    cache: Redis = Depends(get_redis),
    db: Session = Depends(get_db),
):
    try:
        post = crud.get_user_post(db, post_id)
    except Exception as e:
        logger.error(str(e))
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Post does not exist'
        )

    if post.user == current_user:
        message = 'Unable to like own post'
        logger.error(message)
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    if cache.get(f'like:{post_id}:{current_user.id}'):
        message = f'Post {post_id} was already liked by user {current_user.id}'
        logger.error(message)
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=message
        )

    try:
        if cache.get(f'dislike:{post_id}:{current_user.id}'):
            cache.delete(f'dislike:{post_id}:{current_user.id}')
        cache.set(f'like:{post_id}:{current_user.id}', 1)
        
        crud.delete_dislike(db, post.id, current_user.id)
        crud.create_like(db, post.id, current_user.id)
    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error writing like to db'
        )

    return JSONResponse(
        content={'message': f'Post {post_id} liked by {current_user.id}'}
    )


@app.post('/posts/{post_id}/dislike', tags=['posts'])
async def dislike_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    cache: Redis = Depends(get_redis),
    db: Session = Depends(get_db),
):
    try:
        post = crud.get_user_post(db, post_id)
    except Exception as e:
        logger.error(str(e))
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Post does not exist'
        )

    if post.user == current_user:
        message = 'Unable to dislike own post'
        logger.error(message)
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    if cache.get(f'dislike:{post_id}:{current_user.id}'):
        message = f'Post {post_id} was already disliked by user {current_user.id}'
        logger.error(message)
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=message
        )

    try:
        if cache.get(f'like:{post_id}:{current_user.id}'):
            cache.delete(f'like:{post_id}:{current_user.id}')
        cache.set(f'dislike:{post_id}:{current_user.id}', 1)

        crud.delete_like(db, post_id, current_user.id)
        crud.create_dislike(db, post_id, current_user.id)
    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error writing dislike to db'
        )

    return JSONResponse(
        content={'message': f'Post {post_id} disliked by {current_user.id}'}
    )


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings().APP_HOST,
        port=settings().APP_PORT,
        reload=True
    )
