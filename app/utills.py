from passlib.context import CryptContext
import random
import string


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
