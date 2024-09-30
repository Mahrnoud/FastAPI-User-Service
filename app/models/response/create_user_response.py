from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    email: str

    class Config:
        from_attributes = True
