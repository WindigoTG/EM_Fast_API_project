import smtplib
from email.message import EmailMessage

from celery import Celery

from src.config import settings

celery = Celery(
    'tasks',
    broker="redis://:{pwd}@{host}:{port}".format(
        pwd=settings.REDIS_PASSWORD,
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    ),
)


def get_email_template(token: int, account: str):
    email = EmailMessage()
    email["Subject"] = 'Account verification token'
    email["From"] = settings.SMTP_USER
    email["To"] = settings.SMTP_USER
    email.set_content(
        "<div>"
        f"<h3>Here's verification token for {account}</h3>"
        f"<h1>{token}</h1>"
        "</div>",
        subtype="html",
    )
    return email


@celery.task
def send_email_registration_token(token: int, account: str):
    email = get_email_template(token, account)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
