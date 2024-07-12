import jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas, databaseConn, models
# from .config import settings

oauth2_recipient_scheme = OAuth2PasswordBearer(tokenUrl='recipient_login')


# Constants for JWT
SECRET_KEY = "jksownkdnaunrpahfuyenclaybpnwbqa4hei2098453erfgswknifbsxawqin6thfveomcswlxawsbbuy"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


def create_access_token(payload: dict):
    """
    Create a JWT access token.

    Args:
        payload (dict): The payload data to include in the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = payload.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def verify_access_token(token: str, credentials_exception):
    """
    Verify the JWT access token.

    Args:
        token (str): The JWT token to verify.
        credentials_exception (HTTPException): The exception to raise if the token is invalid.

    Returns:
        TokenData: The decoded token data.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        recipient_id: int = payload.get("recipient_id")

        if recipient_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=recipient_id)
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    return token_data


def get_current_recipient(token: str = Depends(oauth2_recipient_scheme), db: Session = Depends(databaseConn.get_db)):
    """
    Retrieve the current user based on the JWT token.

    Args:
        token (str): The JWT token provided in the request.
        db (Session): The database session.

    Returns:
        Donors: The donor object corresponding to the token.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        access_token = verify_access_token(token, credentials_exception)
    except HTTPException as e:
        print(f"Token verification failed: {e.detail}")
        raise

    recipient = db.query(models.Recipients).filter(models.Recipients.id == access_token.id).first()

    # print(access_token.donor_id)
    # print(donor.donor_id)
    if recipient is None:
        print("Recipient not found")
        raise credentials_exception

    return recipient

