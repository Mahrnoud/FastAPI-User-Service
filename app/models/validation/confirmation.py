from pydantic import BaseModel, EmailStr, constr, Field


class ConfirmationCode(BaseModel):
    email: EmailStr = Field(email_regex=r"^[^\s@]+@[^\s@]+\.[^\s@]+$", min_length=10, max_length=254)
    code: constr(min_length=6, max_length=10)
