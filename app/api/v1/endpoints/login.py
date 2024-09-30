from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from ....db.session import get_write_session
from ....repositories.user_repository import UserRepository
from ....services.auth_service import AuthService
from ....services.rate_limiter_service import RateLimiterService
from ....models.validation.login import LoginRequest
from ....services.translation_service import TranslationService
from ....models.response.user import UserResponse

router = APIRouter()

auth_service = AuthService()
user_repo = UserRepository()


@router.post("/login")
async def login(
        login_request: LoginRequest,
        db: AsyncSession = Depends(get_write_session),
        accept_language: str = Header(default=None)
):
    translation_service = TranslationService(locale=accept_language)

    # Initialize the RateLimiterService for login attempts
    rate_limiter = RateLimiterService(
        db=db,
        form_type="login",
        identifier=login_request.email,
        max_attempts=5,
        lockout_minutes=10
    )

    # Check if the user has exceeded the login attempts limit
    if await rate_limiter.is_rate_limited():
        raise HTTPException(
            status_code=429,
            detail={
                "message": translation_service.get("general.too_many_attempts")
            }
        )

    # Authenticate user
    user = await auth_service.authenticate_user(db, login_request.email, login_request.password)

    if not user:
        # If login fails, increment attempts in the rate limiter
        await rate_limiter.increment_attempt()

        raise HTTPException(
            status_code=400,
            detail={
                "message": translation_service.get("login.invalid_credentials"),
            }
        )

    if not user.is_confirmed:
        raise HTTPException(
            status_code=401,
            detail={
                "message": translation_service.get("login.unconfirmed_email"),
                "user": {
                    "email": login_request.email,
                }
            }
        )

    # Reset attempts after successful login
    await rate_limiter.reset_attempt()

    # Generate access token
    access_token = auth_service.create_access_token({
        "sub": user.email,
        "user_id": user.id
    })

    # Use the UserResponse model to return the user data
    return {
        "message": translation_service.get("login.login_success"),
        "access_token": access_token,
        "user": UserResponse.from_orm(user),
    }
