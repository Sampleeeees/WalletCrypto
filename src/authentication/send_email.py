import logging
import emails

from pathlib import Path
from emails.template import JinjaTemplate
from config_fastapi import settings


def send_mail(email_to: str, subject_template="", html_template="", data_send: dict = None) -> None:
    """Відправка email"""
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL)
    )
    print('Host', settings.SMTP_HOST, 'PORT', settings.SMTP_PORT)
    smtp_options = {'host': settings.SMTP_HOST, 'port': settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=data_send, smtp=smtp_options)
    logging.info(f"Send email result: {response}")


def send_new_account_email(email_to: str, username: str) -> None:
    """Відправка повідомлення при реєстрації"""
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Новий акаунт в CryptoWallet для {username}"
    with open(Path(settings.BASE_DIR) / Path(settings.EMAIL_TEMPLATES_DIR) / "success_registration.html") as f:
        template_str = f.read()
    send_mail(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        data_send={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
        },
    )
