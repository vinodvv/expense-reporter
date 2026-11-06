import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, html_body, recipient):
    """Send the report via SMTP."""
    if not config.SENDER_EMAIL or not config.SENDER_PASSWORD:
        raise ValueError("SENDER_EMAIL / SENDER_PASSWORD missing. Check your .env file.")

    recipients = [r.strip() for r in recipient.split(",")]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = config.SENDER_EMAIL
    msg["To"] = ", ".join(recipients)

    # Plain-text fallback + HTML version
    msg.attach(MIMEText("Please view this email in an HTML-capable client.", "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
        server.sendmail(config.SENDER_EMAIL, recipients, msg.as_string())

    print("Email sent to:", ", ".join(recipients))
