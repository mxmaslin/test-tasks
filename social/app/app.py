import aiohttp

import uvicorn

from clearbit import Enrichment
from fastapi import FastAPI, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from settings import settings, Settings
from validators import UserRegistration


app = FastAPI()


@app.post('/auth/register', tags=['auth'])
async def create_user(
    user_registration: UserRegistration,
    settings: Settings = Depends(settings)
):
    
    # Verify email with emailhunter.co
    async with aiohttp.ClientSession() as session:
        url = settings.EMAILHUNTER_URL.format(
            email=user_registration.email,
            api_key=settings.EMAILHUNTER_API_KEY
        )
        async with session.get(url) as response:
            response = await response.json()
            if response.get('result') != 'deliverable':
                raise HTTPException(status_code=400, detail='Invalid email')

        print(response)


#     # Get additional data for the user with clearbit.com
#     enrichment = Enrichment.find(email=user_registration.email, stream=True)
#     if enrichment['person'] is None:
#         raise HTTPException(status_code=400, detail="Invalid email")
#     # Save user data to in-memory database
#     # ...
#     return {"message": "Successfully registered"}


# # User login
# @app.post("/auth/login", tags=["auth"])
# def login(username: str, password: str):
#     # Verify username and password
#     # ...
#     # Create JWT token
#     access_token = AuthJWT.create_access_token(data={"sub": username})
#     return {"access_token": access_token}


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
        app, host=settings().APP_HOST, port=settings().APP_PORT, reload=True
    )
