from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_message(
        booking: dict,
        email_to: EmailStr
) -> EmailMessage:
    email: EmailMessage = EmailMessage()
    email['Subject'] = 'Подтверждение бронирования'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to
    email.set_content(
        f"""
            <h1>Подтверждение бронирования</h1>
            Вы забронировали отель с {booking.get('date_from')} по
             {booking.get('date_to')}
        """,
        subtype='html'
    )
    return email
