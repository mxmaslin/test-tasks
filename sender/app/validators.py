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


class RequestMessageModel(BaseModel):
    status: int
    value: str
    recipient_phone_number: PhoneNumberType


class RequestMailingModel(BaseModel):
    start: str
    end: str
    messages: List[RequestMessageModel]


class ResponseModel(BaseModel):
    error: bool
    error_message: Optional[str] = None
    success_message: Optional[str] = None
