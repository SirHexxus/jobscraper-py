import smtplib
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

SENDER = os.getenv('SENDER')
PASS = os.getenv('PASS')


def send_email(message, receiver):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = SENDER
    receiver_email = receiver
    password = PASS

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        try:
            server.login(sender_email, password)
            res = server.sendmail(sender_email, receiver_email, message)
            print("Email sent!")
        except:
            print("Could not login/send email!")
