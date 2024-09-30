from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.form_submission_attempt_repository import FormSubmissionAttemptRepository


class RateLimiterService:
    def __init__(self, db: AsyncSession, form_type: str, identifier: str, max_attempts: int = 5,
                 lockout_minutes: int = 10):
        self.db = db
        self.form_type = form_type
        self.identifier = identifier
        self.max_attempts = max_attempts
        self.lockout_minutes = lockout_minutes
        self.attempt_repo = FormSubmissionAttemptRepository(db)

    async def is_rate_limited(self):
        """
        Check if the user has exceeded the maximum allowed attempts and if the lockout period is still active.
        """
        attempt = await self.attempt_repo.get_attempt(self.form_type, self.identifier)

        if attempt:
            now = datetime.utcnow()
            lockout_time = attempt.last_attempt + timedelta(minutes=self.lockout_minutes)

            # If the user is within the lockout period
            if attempt.attempts >= self.max_attempts and now < lockout_time:
                return True  # User is still locked out

            # If the user is out of the lockout period, reset attempts and allow retry
            if now >= lockout_time:
                await self.attempt_repo.reset_attempt(attempt)
                return False

        return False  # Not rate-limited

    async def increment_attempt(self):
        """
        Increment the number of attempts for the current form and identifier. Create a record if it doesn't exist.
        """
        attempt = await self.attempt_repo.get_attempt(self.form_type, self.identifier)

        if attempt:
            await self.attempt_repo.increment_attempt(attempt)
        else:
            await self.attempt_repo.create_attempt(self.form_type, self.identifier)

    async def reset_attempt(self):
        """
        Reset the user's attempt count after a successful submission.
        """
        attempt = await self.attempt_repo.get_attempt(self.form_type, self.identifier)
        if attempt:
            await self.attempt_repo.reset_attempt(attempt)
