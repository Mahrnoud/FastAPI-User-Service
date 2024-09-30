from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from ...db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    status = Column(Integer, default=0)
    is_confirmed = Column(Boolean, default=False)
    confirmation_code = Column(String(255), nullable=True)
    password_reset_code = Column(String(255), nullable=True)
    password_reset_code_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
