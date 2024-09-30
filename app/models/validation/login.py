from pydantic import BaseModel, EmailStr, Field, constr


class LoginRequest(BaseModel):
    email: EmailStr = Field(email_regex=r"^[^\s@]+@[^\s@]+\.[^\s@]+$", min_length=10, max_length=254)
    password: constr(min_length=8, max_length=128)
