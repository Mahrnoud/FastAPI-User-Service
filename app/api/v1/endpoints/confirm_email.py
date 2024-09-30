from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from ....repositories.user_repository import UserRepository
from ....db.session import get_write_session
from ....models.validation.confirmation import ConfirmationCode
from ....services.translation_service import TranslationService
from ....services.rate_limiter_service import RateLimiterService

router = APIRouter()
user_repo = UserRepository()


@router.post("/confirm-email")
async def confirm_email(
        confirmation: ConfirmationCode,
        db: AsyncSession = Depends(get_write_session),
        accept_language: str = Header(default=None)
):
    # Load translations based on the user's preferred language
    translation_service = TranslationService(locale=accept_language)

    # Initialize the RateLimiterService for confirmation attempts
    rate_limiter = RateLimiterService(
        db=db,
        form_type="confirm_email",
        identifier=confirmation.email,  # Using the email as identifier
        max_attempts=5,  # Maximum attempts
        lockout_minutes=10  # Lockout duration after max attempts
    )

    # Check if the user has exceeded the confirmation attempts limit
    if await rate_limiter.is_rate_limited():
        raise HTTPException(
            status_code=429,
            detail={
                "message": translation_service.get("general.too_many_attempts")
            }
        )

    # Confirm the user's email using the code
    user = await user_repo.confirm_user_email(db, confirmation.email, confirmation.code)

    if not user:
        # Increment the attempt counter if confirmation fails
        await rate_limiter.increment_attempt()

        raise HTTPException(
            status_code=400,
            detail={
                "message": translation_service.get("general.invalid_code")
            }
        )

    # Reset the attempt counter after successful confirmation
    await rate_limiter.reset_attempt()

    return {
        "message": translation_service.get("confirm_email.confirmation_success")
    }
