from passlib.context import CryptContext
import random
import string

import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import yagmail

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(pass_code: str):
    # Function that hashes the password of each user
    return pwd_context.hash(pass_code)


def verify_passcode(plain_password, hashed_password):
    # Verifies a plain password against a hashed password.
    return pwd_context.verify(plain_password, hashed_password)


# Function to generate a unique alphanumeric serial number
def generate_serial_number():
    # Generate 3 random uppercase letters
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    # Generate 5 random digits
    numbers = ''.join(random.choices(string.digits, k=5))
    # Concatenate the letters and numbers
    return letters + numbers


def send_donation_notification_email(recipient_emails, donation_name, donor_name):
    yag = yagmail.SMTP('drekenzie96@gmail.com', 'ZpgdDrkL4zfq98x')
    body = f'A new donation "{donation_name}" has been made by {donor_name}.'
    yag.send(to=recipient_emails, subject=f'New Donation: {donation_name}', contents=body)


# def send_donation_notification_email(recipient_emails, donation_name, donor_name):
#     email_address = 'drekenzie96@gmail.com'
#     from_password = 'ZpgdDrkL4zfq98x'
#
#     msg = MIMEMultipart()
#     msg['Subject'] = f'New Donation: {donation_name}'
#     msg['From'] = email_address
#     msg['To'] = ', '.join(recipient_emails)
#
#     body = f'A new donation "{donation_name}" has been made by {donor_name}.'
#
#     msg.attach(MIMEText(body, 'plain'))
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login('drekenzie96@gmail.com', 'ZpgdDrkL4zfq98x')
#         smtp.sendmail(msg)
#
