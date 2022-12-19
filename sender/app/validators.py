from pydantic import BaseModel, constr
from typing import List, Optional


PhoneNumberType = constr(regex="^\\+\d{10,29}$")
OpCodeType = constr(regex='^\\+[0-9 ]{1,29}')
TzType = constr(regex='^[a-zA-Z]+/{1}[a-zA-Z]+')


class RequestRecipientModel(BaseModel):
    phone_number: PhoneNumberType
    op_code: OpCodeType
    tz: TzType
    tags: Optional[List[str]]
