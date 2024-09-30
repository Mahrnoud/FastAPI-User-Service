from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from jinja2 import Template
from ....services.email_service import EmailService
from ....services.translation_service import TranslationService
from ....repositories.user_repository import UserRepository
from ....db.session import get_write_session
from ....models.validation.forgot_password import ForgotPasswordRequest
from ....services.rate_limiter_service import RateLimiterService
from ....utils.common import generate_str_code

router = APIRouter()
email_service = EmailService()
user_repo = UserRepository()


@router.post("/forgot-password")
async def forgot_password(
        request: ForgotPasswordRequest,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_write_session),
        accept_language: str = Header(default=None)
):
    # Load translations based on the user's preferred language
    translation_service = TranslationService(locale=accept_language)

    # Initialize RateLimiterService for password reset attempts
    rate_limiter = RateLimiterService(
        db=db,
        form_type="forgot_password",
        identifier=request.email,  # Using the email as identifier
        max_attempts=5,  # Maximum attempts allowed
        lockout_minutes=10  # Lockout duration after max attempts
    )

    # Check if the user has exceeded the password reset request attempts limit
    if await rate_limiter.is_rate_limited():
        raise HTTPException(
            status_code=429,
            detail={
                "message": translation_service.get("general.too_many_attempts")
            }
        )

    # Find the user by email
    user = await user_repo.get_user_by_email(db, request.email)

    if not user:
        # Increment the attempt count if user is not found
        await rate_limiter.increment_attempt()

        raise HTTPException(
            status_code=404,
            detail={
                "message": translation_service.get("general.user_not_found")
            }
        )

    # Generate reset code
    reset_code = generate_str_code()
    user.password_reset_code = reset_code
    user.password_reset_code_expires_at = datetime.utcnow() + timedelta(minutes=10)
    await db.commit()

    # Reset the attempt count after successful request
    await rate_limiter.reset_attempt()

    # Render the reset email using the Jinja2 template
    with open("app/templates/user_reset_password.html") as f:
        template = Template(f.read())
        email_body = template.render(reset_code=reset_code)

    # Queue email sending task
    background_tasks.add_task(
        email_service.send_email,
        user.email,
        "Password Reset",
        email_body
    )

    return {
        "message": translation_service.get("forget_password.reset_code_sent")
    }
