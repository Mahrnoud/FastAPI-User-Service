from sqlalchemy import Column, String, Integer, DateTime
from ...db.session import Base
import datetime


class FormSubmissionAttempt(Base):
    __tablename__ = "form_submission_attempts"

    id = Column(Integer, primary_key=True, index=True)
    form_type = Column(String(50), nullable=False)  # e.g., login, registration
    identifier = Column(String(255), nullable=False)  # Email or IP
    attempts = Column(Integer, default=0)
    last_attempt = Column(DateTime, default=datetime.datetime.utcnow)
