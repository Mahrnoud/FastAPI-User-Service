from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.models.form_submission_attempts import FormSubmissionAttempt


class FormSubmissionAttemptRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_attempt(self, form_type: str, identifier: str):
        result = await self.db.execute(
            select(FormSubmissionAttempt)
            .where(FormSubmissionAttempt.form_type == form_type)
            .where(FormSubmissionAttempt.identifier == identifier)
        )
        return result.scalars().first()

    async def increment_attempt(self, attempt: FormSubmissionAttempt):
        attempt.attempts += 1
        attempt.last_attempt = datetime.utcnow()
        self.db.add(attempt)
        await self.db.commit()

    async def create_attempt(self, form_type: str, identifier: str):
        new_attempt = FormSubmissionAttempt(
            form_type=form_type,
            identifier=identifier,
            attempts=1,
            last_attempt=datetime.utcnow(),
        )
        self.db.add(new_attempt)
        await self.db.commit()
        return new_attempt

    async def reset_attempt(self, attempt: FormSubmissionAttempt):
        attempt.attempts = 0
        self.db.add(attempt)
        await self.db.commit()
