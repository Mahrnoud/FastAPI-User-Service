from pydantic import BaseModel, EmailStr, Field


class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(email_regex=r"^[^\s@]+@[^\s@]+\.[^\s@]+$", min_length=10, max_length=254)
