import aiosmtplib
from email.mime.text import MIMEText
from jinja2 import Template
from ..core.config import settings


class EmailService:
    async def send_email(self, to_email: str, subject: str, body: str):
        message = MIMEText(body, "html")
        message["From"] = settings.SMTP_FROM_EMAIL
        message["To"] = to_email
        message["Subject"] = subject

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            start_tls=True,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD
        )

    async def send_confirmation_email(self, email: str, confirmation_code: str):
        # Render the confirmation email template
        with open("app/templates/user_email_confirmation.html") as f:
            template = Template(f.read())
            email_body = template.render(confirmation_code=confirmation_code)

        await self.send_email(email, "Email Confirmation", email_body)

    async def send_reset_password_email(self, email: str, reset_code: str):
        # Render the reset password email template
        with open("app/templates/user_reset_password.html") as f:
            template = Template(f.read())
            email_body = template.render(reset_code=reset_code)

        await self.send_email(email, "Password Reset", email_body)
