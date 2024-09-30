from pydantic import BaseModel
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    status: int
    is_confirmed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
