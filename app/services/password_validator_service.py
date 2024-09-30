import re
from fastapi import HTTPException
from ..services.translation_service import TranslationService


class PasswordValidatorService:
    def __init__(self, password: str, translation_service: TranslationService):
        self.password = password
        self.translation_service = translation_service

    def validate(self):
        self.check_length()
        self.check_upper_lower_case()
        self.check_numeric()
        self.check_special_characters()
        self.check_common_patterns()

    def check_length(self):
        if len(self.password) < 8:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": self.translation_service.get("password.too_short")
                }
            )

    def check_upper_lower_case(self):
        if not re.search(r'[A-Z]', self.password) or not re.search(r'[a-z]', self.password):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": self.translation_service.get("password.missing_case")
                }
            )

    def check_numeric(self):
        if not re.search(r'[0-9]', self.password):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": self.translation_service.get("password.missing_number")
                }
            )

    def check_special_characters(self):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', self.password):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": self.translation_service.get("password.missing_special")
                }
            )

    def check_common_patterns(self):
        # Add checks for common weak patterns like "password123", "qwerty", etc.
        weak_patterns = ['password', '123456', 'qwerty', 'letmein', 'admin']
        if any(pattern in self.password.lower() for pattern in weak_patterns):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": self.translation_service.get("password.common_password")
                }
            )
