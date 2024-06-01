from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..databaseConn import get_db
from .. import models, schemas, utills, oauth2

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/donor_login")
def donor_login(donor_credentials: schemas.DonorLogin, db: Session = Depends(get_db)):
    """
    Handle donor login and token generation.

    Args:
        donor_credentials (schemas.DonorLogin): The donor's login credentials.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary containing the access token and its type.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    donor = db.query(models.DonorCredentials).filter(models.DonorCredentials.username == donor_credentials.username).first()

    if not donor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utills.verify_passcode(donor_credentials.password, donor.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(payload={"donor_id": donor.id})
    return {"access token": access_token, "token type": "bearer"}