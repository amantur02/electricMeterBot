from pydantic import BaseModel


class Resident(BaseModel):
    house_number: str = None
    user_name: str = None
    phone_number: str = None
