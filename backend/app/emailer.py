from __future__ import annotations

import smtplib
import ssl
from email.message import EmailMessage

from .config import Settings


TEST_EMAIL_BODY = "este es un correo de prueba de Unisan Payroll"


def send_test_email(settings: Settings) -> str:
    username = settings.smtp_username
    password = settings.smtp_password
    sender = settings.smtp_from or username
    recipient = settings.smtp_test_recipient
    if not username or not password or not sender or not recipient:
        raise ValueError("La configuración SMTP está incompleta.")

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = "Correo de prueba - Unisan Payroll"
    message.set_content(TEST_EMAIL_BODY)

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()
        smtp.login(username, password)
        smtp.send_message(message)
    return recipient


def send_settlement_email(
    settings: Settings,
    *,
    recipient: str,
    recipient_name: str,
    pdf_content: bytes,
    pdf_file_name: str,
    subject: str = "Liquidación - Unisan Payroll",
    body: str = "este es un correo de prueba de Unisan Payroll",
) -> str:
    username = settings.smtp_username
    password = settings.smtp_password
    sender = settings.smtp_from or username
    if not username or not password or not sender:
        raise ValueError("La configuración SMTP está incompleta.")
    if not recipient:
        raise ValueError("El trabajador seleccionado no tiene correo registrado.")

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)
    message.add_attachment(
        pdf_content,
        maintype="application",
        subtype="pdf",
        filename=pdf_file_name,
    )

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()
        smtp.login(username, password)
        smtp.send_message(message)
    return recipient
