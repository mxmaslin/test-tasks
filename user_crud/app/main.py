import sys

from pathlib import Path

import uvicorn

from dadata import Dadata
from fastapi import Depends, FastAPI, HTTPException, status, Response
from fastapi.responses import JSONResponse
from redis import Redis
from sqlalchemy.orm import Session

app_path = Path.cwd()
sys.path.append(str(app_path))

import crud
from app.constants import CACHE_KEY
from app.dependencies import get_redis, get_db, get_dadata
from app.logger import logger
from app.schemas import UserGet, UserCreate, UserDelete
from app.models import User
from app.settings import settings

app = FastAPI()


@app.post('/save_user_data', tags=['users'])
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
    dadata: Dadata = Depends(get_dadata),
) -> JSONResponse:
    country_code = cache.get(CACHE_KEY.format(user_data.country))
    if country_code is None:
        country_code = dadata.suggest(
            'country', user_data.country
        )[0].get('data', {}).get('alfa3')
        cache.set(CACHE_KEY.format(user_data.country), country_code)
    try:
        user = crud.create_user(db, user_data.dict())
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error writing user to db'
        )

    return JSONResponse(content={'message': f'User {user.phone_number} created'})


@app.post('/get_user_data', tags=['users'])
async def get_user(
    user_phone: UserGet,
    db: Session = Depends(get_db),
) -> JSONResponse:
    user: User = crud.get_user(db, user_phone)
    if user is None:
        logger.error(str(f'User {user_phone} does not exist'))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return JSONResponse(content={
        'message': {
            'phone_number': user.phone_number,
            'name': user.phone_number,
            'surname': user.surname,
            'patronymic': user.patronymic,
            'phone_number': user.phone_number,
            'country_code': user.country
        }
    })


@app.post('/delete_user_data', tags=['users'])
def delete_user(
    user_phone: UserDelete, db: Session = Depends(get_db),
) -> JSONResponse:
    try:
        crud.delete_user(db, user_phone)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error deleting user from db'
        )
    return JSONResponse(content={'message': f'User {user_phone} deleted'})


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings().APP_HOST,
        port=settings().APP_PORT,
        reload=True
    )
