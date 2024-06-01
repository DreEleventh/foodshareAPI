from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session

from .. import models, schemas, utills
from ..databaseConn import get_db

router = APIRouter(
    prefix="/donation_header",
    tags=["Donation Headers"]
)


# donation header endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DonationHeaderResponse)
def create_donation_herder(donation_header: schemas.MakeDonationHeader, db: Session = Depends(get_db)):
    # Generate unique serial number
    serial_number = utills.generate_serial_number()

    while (db.query(models.DonationHeader).filter(models.DonationHeader.serial_number == serial_number)
                   .first() is not None):
        serial_number = utills.generate_serial_number()

    # Convert Pydantic model to dictionary
    donation_data = donation_header.dict()
    # Add the generated serial number to the data dictionary
    donation_data['serial_number'] = serial_number

    new_donation_header = models.DonationHeader(**donation_data)

    db.add(new_donation_header)
    db.commit()
    db.refresh(new_donation_header)

    return new_donation_header


# Get all donation header endpoint
@router.get("/", response_model=List[schemas.DonationHeaderResponse])
def get_donation_headers(db: Session = Depends(get_db)):

    headers = db.query(models.DonationHeader).order_by(models.DonationHeader.id.desc()).all()

    donation_header_dict = [header.__dict__ for header in headers]

    return donation_header_dict


# Get a single donation header by id
@router.get("/{header_id}")
def get_header_by_id(header_id: int, db: Session = Depends(get_db)):
    single_header = (db.query(models.DonationHeader).filter(models.DonationHeader.id == header_id)
                     .order_by(models.DonationHeader.id.asc()).first())

    if not single_header:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation header with id {header_id} does not exist")

    return single_header


# Delete a donation header endpoint
@router.delete("/{header_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_header(header_id: int, db: Session = Depends(get_db)):

    remove_header = db.query(models.DonationHeader).filter(models.DonationHeader.id == header_id).first()

    if remove_header is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation header with id {header_id} not found")

    db.delete(remove_header)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a donation header endpoint
@router.put("/{header_id}")
def update_header(header_id: int, header_update: schemas.MakeDonationHeader, db: Session = Depends(get_db)):
    update_query = db.query(models.DonationHeader).filter(models.DonationHeader.id == header_id)

    header = update_query.first()

    if header is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation header with id {header_id} not found")

    update_query.update(header_update.dict(), synchronize_session=False)
    db.commit()

    return {"message": f"Donation with id {header_id} successfully updated"}

