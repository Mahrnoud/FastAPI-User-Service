from fastapi import APIRouter, Depends, HTTPException, Header
from ....db.session import get_read_session
from ....repositories.user_repository import UserRepository
from ....core.auth import get_current_user
from ....db.models import user
from ....services.translation_service import TranslationService
from ....models.response.user import UserResponse

router = APIRouter()
user_repo = UserRepository()


@router.get("/profile")
async def get_profile(
        current_user: user = Depends(get_current_user),
        db=Depends(get_read_session),
        accept_language: str = Header(default=None)
):
    # Load translations based on the user's preferred language
    translation_service = TranslationService(locale=accept_language)

    user_data = await user_repo.get_user_by_id(db, current_user.id)

    if not user_data:
        raise HTTPException(
            status_code=404,
            detail={
                "message": translation_service.get("general.user_not_found"),
            }
        )

    return UserResponse.from_orm(user_data)
