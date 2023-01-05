from pydantic import BaseModel
from typing import List, Optional


class UserModel(BaseModel):
    first_name = str
    second_name = str
    username = str


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
    data: Optional[List] = []


class ResponseSuccessModel(ResponseModel):
    class Config:
        schema_extra = {
            'example': {
                'data': [],
                'error': False,
                'error_message': None,
                'success_message': 'Operation success'
            }
        }


class ResponseFailureModel(ResponseModel):
    class Config:
        schema_extra = {
            'example': {
                'data': [],
                'error': True,
                'error_message': 'Operation failure',
                'success_message': None
            }
        }
