import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


def send_mail(to, subject, body, html_body=None):

    try:

        print("MAIL_USERNAME:", MAIL_USERNAME)
        print("MAIL_PASSWORD LOADED:", bool(MAIL_PASSWORD))

        if not MAIL_USERNAME or not MAIL_PASSWORD:
            print("MAIL ERROR: MAIL_USERNAME or MAIL_PASSWORD not configured")
            return False

        msg = EmailMessage()

        msg["From"] = MAIL_USERNAME
        msg["To"] = to
        msg["Subject"] = subject

        msg.set_content(body)

        if html_body:
            msg.add_alternative(
                html_body,
                subtype="html"
            )

        print("Connecting to Gmail SMTP...")

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as server:

            print("Connected to Gmail SMTP")

            server.login(
                MAIL_USERNAME,
                MAIL_PASSWORD
            )

            print("Gmail Login Successful")

            server.send_message(msg)

        print(f"Mail Sent Successfully To: {to}")

        return True

    except Exception as e:

        print("MAIL ERROR:", repr(e))

        return False