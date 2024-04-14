from email.message import EmailMessage
from smtplib import SMTP_SSL

from pydantic import EmailStr

from app.tasks.celery import celery_app
from app.tasks.email_templates import create_booking_confirmation_message
from app.config import settings


@celery_app.task
def send_booking_confirmation_email(
    booking: dict,
    mail_to: EmailStr
) -> None:
    mail_to = settings.SMTP_USER if settings.MODE == 'DEV' else mail_to

    msg: EmailMessage = create_booking_confirmation_message(booking, mail_to)
    with SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
