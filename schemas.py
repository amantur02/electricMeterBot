from pydantic import BaseModel


class Resident(BaseModel):
    home_number: str = None
    user_name: str = None
    phone_number: str = None
