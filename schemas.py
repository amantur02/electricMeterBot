from pydantic import BaseModel


class Resident(BaseModel):
    home_number: str = None
    user_name: str = None
    phone_number: str = None


class Electricity(BaseModel):
    resident_id: int = None
    current_kwh: int = None
    consumed_kwh: int = None
    increased_kwh: int = None
    payment_status: bool = None
    amount: float = None
    increased_amount: float = None
    not_increased_amount: float = None
