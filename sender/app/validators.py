from datetime import datetime

from pydantic import BaseModel, constr
from typing import List, Optional


PhoneNumberType = constr(regex="^\\+\d{10,29}$")
OpCodeType = constr(regex='^\\+[0-9 ]{1,29}')
TzType = constr(regex='^[a-zA-Z]+/{1}[a-zA-Z]+')


class RequestRecipientModel(BaseModel):
    phone_number: PhoneNumberType
    op_code: Optional[OpCodeType]
    tz: Optional[TzType]
    tags: Optional[List[str]]

    class Config:
        schema_extra = {
            'example': {
               'phone_number': '+79261234567',
               'op_code': '+375',
               'tz': 'Europe/Moscow',
               'tags': ['wow', 'amazing guy', 'so cool']
            }
        }


class RequestMessageModel(BaseModel):
    status: int
    value: str
    recipient_phone_number: PhoneNumberType


class RequestMailingModel(BaseModel):
    start: str
    end: str
    messages: List[RequestMessageModel]

    class Config:
        schema_extra = {
            'example': {
                'start': '2021-04-23T10:20:30.400+02:30',
                'end': '2023-04-23T10:20:30.400+02:30',
                'messages': [
                    {
                        'status': 0,
                        'value': 'Добрый вечер',
                        "recipient_phone_number": '+79261234567'
                    },
                    {
                        'status': 0,
                        'value': 'Доброе утро',
                        'recipient_phone_number': '+79261234567'
                    }
                ]
            }
        }


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
