from pydantic import BaseModel
from typing import Dict, List, Optional


class LoginModel(BaseModel):
    username: str
    password: str


class CreatePersonModel(BaseModel):
    first_name: str
    second_name: str
    username: str
    password: str


class UpdatePersonModel(BaseModel):
    first_name: Optional[str]
    second_name: Optional[str]
    username: Optional[str]
    password: Optional[str]


class ApartmentModel(BaseModel):
    room_number: int


class BookingModel(BaseModel):
    start_date: str
    end_date: str
    person: List[str]
    booking: List[int]


class ResponseModel(BaseModel):
    error: bool
    error_message: Optional[str] = None
    success_message: Optional[str] = None
    data: Optional[Dict] = {}


class ResponseSuccessModel(ResponseModel):
    class Config:
        schema_extra = {
            'example': {
                'error': False,
                'error_message': None,
                'success_message': 'Operation success'
            }
        }


class ResponseFailureModel(ResponseModel):
    class Config:
        schema_extra = {
            'example': {
                'error': True,
                'error_message': 'Operation failure',
                'success_message': None
            }
        }
