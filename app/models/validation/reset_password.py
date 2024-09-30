from pydantic import BaseModel, constr


class ResetPasswordRequest(BaseModel):
    new_password: constr(min_length=8, max_length=128)
