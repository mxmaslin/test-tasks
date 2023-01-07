from pydantic import BaseModel
from datetime import date
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
    start_date: date
    end_date: date
    person_ids: List[int]
    apartment_id: int


class UpdateBookingModel(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    person_id: Optional[int]
    apartment_id: Optional[int]


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
