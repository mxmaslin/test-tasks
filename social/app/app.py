from datetime import timedelta

import aiohttp

import uvicorn

from clearbit import Enrichment
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi_jwt_auth import AuthJWT

from auth import authenticate_user, create_access_token
from settings import settings, Settings
from validators import UserLoginModel


app = FastAPI()


@app.post('/token', tags=['auth'])
async def login_for_access_token(
    user_data: UserLoginModel,
    settings: Settings = Depends(settings)
):

    # import bcrypt
    # password = user_data.password.encode('utf-8')
    # hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    # print(hashed)

    # Verify email with emailhunter.co
    async with aiohttp.ClientSession() as session:
        url = settings.EMAILHUNTER_URL.format(
            email=user_data.email,
            api_key=settings.EMAILHUNTER_API_KEY
        )
        async with session.get(url) as response:
            response = await response.json()
            if response.get('result') != 'deliverable':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Invalid email'
                )

    user = authenticate_user(user_data.email, user_data.password)
    if not user:
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
    return {'access_token': access_token, 'token_type': 'bearer'}



#     # Get additional data for the user with clearbit.com
#     enrichment = Enrichment.find(email=user_registration.email, stream=True)
#     if enrichment['person'] is None:
#         raise HTTPException(status_code=400, detail="Invalid email")
#     # Save user data to in-memory database
#     # ...
#     return {"message": "Successfully registered"}


# # Post creation, editing, deletion and viewing
# @app.get("/posts")
# def read_posts(current_user: str = Depends(AuthJWT.get_current_user)):
#     # Get all posts from in-memory database
#     # ...
#     return {"posts": posts}


# @app.post("/posts", status_code=201)
# def create_post(post: str, current_user: str = Depends(AuthJWT.get_current_user)):
#     # Save post to in-memory database
#     # ...
#     return {"message": "Post created"}


# @app.put("/posts/{post_id}")
# def update_post(post_id: int, post: str, current_user: str = Depends(AuthJWT.get_current_user)):
#     # Update post in in-memory database
#     # ...
#     return {"message": "Post updated"}


# @app.delete("/posts/{post_id}", status_code=204)
# def delete_post(post_id: int, current_user: str = Depends(AuthJWT.get_current_user)):
#     # Delete post from in-memory database
#     # ...
#     return


# # Post likes and dislikes
# @app.post("/posts/{post_


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=settings().APP_HOST,
        port=settings().APP_PORT,
        reload=True
    )
