import os
from pathlib import Path
from aiosmtplib import SMTP
from pydantic_settings import BaseSettings
from loguru import logger


class MailSettings(BaseSettings):
    mail_server: str = 'smtp.gmail.com'
    mail_port: int = 587
    mail_username: str
    mail_password: str


settings = MailSettings()
templates_folder = Path(os.path.dirname(__file__)) / '../assets'


def _load_forgot_password_template(restore_code):
    with open(templates_folder / 'forgot_password_email.html') as f:
        text = f.read()
    return text.format(restore_code=restore_code)


async def _send_email(client, recipient_email: str, message: str):
    try:
        async with client:
            await client.sendmail(settings.mail_username, [recipient_email], message)
    except Exception as e:
        logger.error(str(e))


async def send_forgot_password_mail(recipient_email: str, restore_code: str):
    smtp_client = SMTP(
        hostname=settings.mail_server,
        port=settings.mail_port,
        use_tls=True,
        username=settings.mail_username,
        password=settings.mail_password
    )
    message = _load_forgot_password_template(restore_code)
    await _send_email(smtp_client, recipient_email, message)

