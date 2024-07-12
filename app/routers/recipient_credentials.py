from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session

from .. import models, schemas, utills, oauth2
from ..databaseConn import get_db

router = APIRouter(
    prefix="/recipient_credentials",
    tags=["Recipient Credentials"]
)


# Create recipient credentials endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RecipientCredentialsResponse)
def create_recipient_credentials(recip_cred: schemas.RecipientCredentials, db: Session = Depends(get_db)):
    # Hash user password - recio_cred.password
    hashed_password = utills.hash_password(recip_cred.password)
    recip_cred.password = hashed_password

    new_recip_cred = models.RecipientCredentials(**recip_cred.dict())
    db.add(new_recip_cred)
    db.commit()
    db.refresh(new_recip_cred)

    return new_recip_cred


