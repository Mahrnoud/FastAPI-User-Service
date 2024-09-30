from pydantic import BaseModel, EmailStr, constr, Field


class UserCreate(BaseModel):
    first_name: constr(min_length=3, max_length=64)
    last_name: constr(min_length=3, max_length=64)
    email: EmailStr = Field(email_regex=r"^[^\s@]+@[^\s@]+\.[^\s@]+$", min_length=10, max_length=254)
    password: constr(min_length=8, max_length=128)
