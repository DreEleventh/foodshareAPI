from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utills
from ..databaseConn import get_db

router = APIRouter(
    prefix="/donor_credentials",
    tags=["Donor Credentials"],
)


# create donor credentials endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DonorCredentialsResponse)
def create_donor_credentials(donor_cred: schemas.DonorCredentials, db: Session = Depends(get_db)):

    # Hash user password - donor_cred.password
    hashed_password = utills.hash_password(donor_cred.password)
    donor_cred.password = hashed_password

    new_donor_cred = models.DonorCredentials(**donor_cred.dict())
    db.add(new_donor_cred)
    db.commit()
    db.refresh(new_donor_cred)

    return new_donor_cred

