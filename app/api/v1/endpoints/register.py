from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Header
from ....services.email_service import EmailService
from ....repositories.user_repository import UserRepository
from ....db.session import get_write_session
from ....core.hashing import get_password_hash
from ....models.validation.register import UserCreate
from ....models.response.create_user_response import CreateUserResponse
from ....services.translation_service import TranslationService
from ....services.rate_limiter_service import RateLimiterService
from ....services.password_validator_service import PasswordValidatorService
from ....utils.common import generate_int_code
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
email_service = EmailService()
user_repo = UserRepository()


@router.post("/register")
async def register(
        user: UserCreate,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_write_session),
        accept_language: str = Header(default=None)
):
    # Load translations based on the user's preferred language
    translation_service = TranslationService(locale=accept_language)

    # Rate limiting for the registration form
    rate_limiter = RateLimiterService(
        db=db,
        form_type="registration",
        identifier=user.email
    )

    # Check if the user has exceeded the registration attempts limit
    if await rate_limiter.is_rate_limited():
        raise HTTPException(
            status_code=429,
            detail={
                "message": translation_service.get("general.too_many_attempts")
            }
        )

    # Check if the email already exists
    existing_user = await user_repo.get_user_by_email(db, user.email)

    if existing_user:
        # Increment attempt count if email already exists
        await rate_limiter.increment_attempt()

        raise HTTPException(
            status_code=400,
            detail={
                "message": translation_service.get("register.registered_email")
            }
        )

    # Validate password strength
    password_validator = PasswordValidatorService(
        password=user.password,
        translation_service=translation_service
    )
    password_validator.validate()  # Raises exception if the password is weak

    # Create new user
    hashed_password = get_password_hash(user.password)
    confirmation_code = generate_int_code()

    await user_repo.create_user(
        db=db,
        user_data={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "hashed_password": hashed_password,
            "confirmation_code": confirmation_code,
        }
    )

    # Reset attempts after successful registration
    await rate_limiter.reset_attempt()

    # Send confirmation email
    background_tasks.add_task(
        email_service.send_confirmation_email,
        user.email,
        confirmation_code
    )

    return {
        "message": translation_service.get("register.register_success"),
        "user": CreateUserResponse.from_orm(user),
    }
