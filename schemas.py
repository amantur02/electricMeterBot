from typing import Optional

from pydantic import BaseModel


class Resident(BaseModel):
    home_number: str = None
    user_name: str = None
    phone_number: str = None


class Electricity(BaseModel):
    resident_id: Optional[int] = None
    current_kwh: Optional[int] = None
    consumed_kwh: Optional[int] = None
    increased_kwh: Optional[int] = None
    payment_status: Optional[bool] = None
    amount: Optional[float] = None
    increased_amount: Optional[float] = None
    not_increased_amount: Optional[float] = None

    class Config:
        from_attributes = True

