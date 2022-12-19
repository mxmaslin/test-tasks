from pydantic import BaseModel, constr
from typing import List, Optional


MyPhoneNumberType = constr(regex="^\\+\d{10,29}$")


class RequestRecipientModel(BaseModel):
    phone_number: MyPhoneNumberType
    op_code: str
    tz: str
    tag: Optional[List[str]]
