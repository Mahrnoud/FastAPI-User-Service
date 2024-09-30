from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..core.config import settings
from ..core.hashing import verify_password
from ..repositories.user_repository import UserRepository

user_repo = UserRepository()


class AuthService:
    async def authenticate_user(self, db, email: str, password: str):
        user = await user_repo.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
