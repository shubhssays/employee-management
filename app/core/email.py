import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings
from app.core.logging import get_logger
from app.shared.schemas.email import EmailPayload

SMTP_SERVER = settings.SMTP_SERVER
SMTP_PORT = settings.SMTP_PORT
SENDER_EMAIL = settings.SENDER_EMAIL
SENDER_PASSWORD = settings.SENDER_APP_PASSWORD

logger = get_logger(__name__)


def send_email(payload: EmailPayload) -> None:
    """
    Send an email using the configured SMTP server.

    The SMTP connection is created for each email and closed
    automatically after sending.
    """

    text_body = payload.get("text_body")
    html_body = payload.get("html_body")
    receiver_email = payload.get("receiver_email")
    subject = payload.get("subject")
    complete_filepath = payload.get("complete_filepath")

    # Validate required fields
    if text_body is None and html_body is None:
        raise ValueError("Either 'text_body' or 'html_body' is required")

    # ---------------------------------------------------------
    # Create email message
    # ---------------------------------------------------------

    message = MIMEMultipart("mixed")

    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = subject

    # ---------------------------------------------------------
    # Add email body
    # ---------------------------------------------------------

    if text_body is not None and html_body is not None:
        # Multipart alternative allows email clients to choose
        # either the plain-text or HTML version.
        body = MIMEMultipart("alternative")

        body.attach(MIMEText(text_body, "plain", "utf-8"))
        body.attach(MIMEText(html_body, "html", "utf-8"))

        message.attach(body)

    elif html_body is not None:
        message.attach(MIMEText(html_body, "html", "utf-8"))

    else:
        message.attach(MIMEText(text_body, "plain", "utf-8"))

    # ---------------------------------------------------------
    # Add attachment
    # ---------------------------------------------------------

    if complete_filepath:
        if not os.path.isfile(complete_filepath):
            raise FileNotFoundError(
                f"Attachment file not found: {complete_filepath}"
            )

        try:
            with open(complete_filepath, "rb") as attachment_file:
                attachment = MIMEBase("application", "octet-stream")
                attachment.set_payload(attachment_file.read())

            encoders.encode_base64(attachment)

            filename = os.path.basename(complete_filepath)

            attachment.add_header(
                "Content-Disposition",
                "attachment",
                filename=filename,
            )

            message.attach(attachment)

            logger.info(
                "Successfully attached file: %s",
                complete_filepath,
            )

        except OSError:
            logger.exception(
                "Failed to read attachment: %s",
                complete_filepath,
            )
            raise

    # ---------------------------------------------------------
    # Connect to SMTP server and send email
    # ---------------------------------------------------------

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login(SENDER_EMAIL, SENDER_PASSWORD)

            logger.info(
                "SMTP login successful. Sending email to %s",
                receiver_email,
            )

            server.send_message(
                message,
                from_addr=SENDER_EMAIL,
                to_addrs=[receiver_email],
            )

            logger.info(
                "Email successfully sent to %s",
                receiver_email,
            )

    except smtplib.SMTPException:
        logger.exception(
            "SMTP error while sending email to %s",
            receiver_email,
        )
        raise
