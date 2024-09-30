from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.models.user import User


class UserRepository:
    async def create_user(self, db: AsyncSession, user_data: dict) -> User:
        user = User(**user_data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_reset_code(self, db: AsyncSession, code: str) -> User:
        result = await db.execute(select(User).where(User.password_reset_code == code))
        return result.scalar_one_or_none()

    async def confirm_user_email(self, db, email: str, confirmation_code: str):
        user = await db.execute(select(User).where(User.email == email, User.confirmation_code == confirmation_code))
        user = user.scalars().first()
        if user:
            user.is_confirmed = True
            user.confirmation_code = ''
            db.add(user)
            await db.commit()
            return user
        return None
