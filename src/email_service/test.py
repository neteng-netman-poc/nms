from email_sender import EmailSender
import os


def main():
    """Simple test runner that sends an email using EmailSender.send_to_recipient.

    Make sure the following environment variables are set (for example in a .env file):
      - email (sender email)
      - apppassword (smtp/app password)
      - receipt_email (recipient email)

    Run this file and let me know whether you receive the email.
    """

    subject = os.getenv("TEST_SUBJECT", "Test email from EmailSender")
    content = os.getenv(
        "TEST_CONTENT", "This is a test email sent by EmailSender.send_to_recipient"
    )

    es = EmailSender()

    try:
        print(
            f"Sending -> from: {es.email_id}  to: {es.receipt_email_id}  subject: {subject}"
        )
        es.send_to_recipient(subject=subject, content=content)
        print(
            "Send attempted — if SMTP credentials are correct, the recipient should receive the message."
        )
    except Exception as e:
        print("Error while sending email:", repr(e))

    try:
        print(
            f"Sending -> from: {es.email_id}  to: dheeraj.cuboulder@gmail.com  subject: {subject}"
        )
        es.send_to_custom_recipient(
            target_email="dheeraj.cuboulder@gmail.com", subject=subject, content=content
        )
        print(
            "Send attempted — if SMTP credentials are correct, the recipient should receive the message."
        )
    except Exception as e:
        print("Error while sending email:", repr(e))


if __name__ == "__main__":
    main()
