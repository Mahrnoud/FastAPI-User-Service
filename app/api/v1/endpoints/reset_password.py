from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from ....repositories.user_repository import UserRepository
from ....db.session import get_write_session
from ....core.hashing import get_password_hash
from ....models.validation.reset_password import ResetPasswordRequest
from ....services.translation_service import TranslationService
from ....services.rate_limiter_service import RateLimiterService
from ....services.password_validator_service import PasswordValidatorService
from pydantic import constr

router = APIRouter()
user_repo = UserRepository()


@router.post("/reset-password/{code}")
async def set_new_password(
        code: constr(min_length=16, max_length=16, pattern=r'^[a-zA-Z0-9]+$'),
        request: ResetPasswordRequest,
        db: AsyncSession = Depends(get_write_session),
        accept_language: str = Header(default=None)
):
    # Load translations based on the user's preferred language
    translation_service = TranslationService(locale=accept_language)

    # Retrieve user by confirmation code
    user = await user_repo.get_user_by_reset_code(db, code)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "message": translation_service.get("general.invalid_code")
            },
        )

    # Initialize RateLimiterService for reset password attempts
    rate_limiter = RateLimiterService(
        db=db,
        form_type="reset_password",
        identifier=user.email,  # Using the email as identifier
        max_attempts=5,  # Maximum attempts allowed
        lockout_minutes=10  # Lockout duration after max attempts
    )

    # Check if the user has exceeded the password reset attempts limit
    if await rate_limiter.is_rate_limited():
        raise HTTPException(
            status_code=429,
            detail={
                "message": translation_service.get("general.too_many_attempts")
            }
        )

    # Check if the reset code has expired
    if user.password_reset_code_expires_at and user.password_reset_code_expires_at < datetime.utcnow():
        # Increment attempt if reset code is invalid
        await rate_limiter.increment_attempt()

        raise HTTPException(
            status_code=400,
            detail={"message": translation_service.get("reset_password.code_expired")}
        )

    # Validate reset code
    if user.password_reset_code != code:
        # Increment attempt if reset code is invalid
        await rate_limiter.increment_attempt()

        raise HTTPException(
            status_code=400,
            detail={
                "message": translation_service.get("general.invalid_code")
            }
        )

    # Validate password strength
    password_validator = PasswordValidatorService(
        password=request.new_password,
        translation_service=translation_service
    )
    password_validator.validate()  # Raises exception if the password is weak

    # Hash the new password and update user information
    user.hashed_password = get_password_hash(request.new_password)
    user.is_confirmed = 1
    user.confirmation_code = None
    user.password_reset_code = None
    user.password_reset_code_expires_at = None
    await db.commit()

    # Reset attempts after successful password reset
    await rate_limiter.reset_attempt()

    return {
        "message": translation_service.get("reset_password.reset_success")
    }
