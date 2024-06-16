from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session

from .. import models, schemas, utills, oauth2
from ..databaseConn import get_db

router = APIRouter(
    prefix="/donors",
    tags=["Donors"],
)


# Donor registration endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DonorResponse)
def register_donor(donor: schemas.RegisterDonor, db: Session = Depends(get_db)):
    """
    Endpoint to register a new donor.
    """
    try:
        new_donor = models.Donors(**donor.dict())
        db.add(new_donor)
        db.commit()
        db.refresh(new_donor)

        if new_donor:
            return new_donor
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed tp create donor.")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Get all donors endpoint
@router.get("/")
def display_all_donors(db: Session = Depends(get_db)):
    """
    Endpoint to get all donors.
    """
    donors = db.query(models.Donors).order_by(models.Donors.id.asc()).all()
    return donors


# Get the current logged in donor
@router.get("/user/")
def fetch_current_donor(db: Session = Depends(get_db),
                        current_donor: models.Donors = Depends(oauth2.get_current_user)):
    """
    Endpoint to get the current logged in user.
    """
    fetch_donor = db.query(models.Donors).filter(models.Donors.id ==
                                                 current_donor.id).order_by(models.Donors.id.asc()).first()

    if fetch_donor.id != current_donor.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action.")

    return fetch_donor


# Get donor by id endpoint
@router.get("/{donor_id}")
def get_donor_by_id(donor_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get a donor by its ID.
    """
    single_donor = db.query(models.Donors).filter(models.Donors.id == donor_id).order_by(models.Donors.id.asc()).first()

    if single_donor:
        return single_donor
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation with id: {donor_id} does not exist")


# Delete a donor by ID endpoint
@router.delete("/{donor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_donor_by_id(donor_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a donor by its ID.
    """
    remove_donor = db.query(models.Donors).filter(models.Donors.id == donor_id).first()

    if remove_donor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation with id: {donor_id} does not exist")

    db.delete(remove_donor)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a donor endpoint
@router.put("/{donor_id}")
def update_donor(donor_id: int, donor_update: schemas.RegisterDonor, db: Session = Depends(get_db)):
    """
    Endpoint to update a donor by its ID.
    """
    update_query = db.query(models.Donors).filter(models.Donors.id == donor_id)

    donor = update_query.first()

    if donor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Donor with id: {donor_id} does not exist")

    update_query.update(donor_update.dict(), synchronize_session=False)
    db.commit()

    return {"message": f"Donor with id: {donor_id} successfully updated"}

# # Donor type endpoint
# @app.get("/donor_type")
# def get_all_donor_types(db: Session = Depends(get_db)):
#     """
#     Endpoint to get all donor types.
#     """
#     donor_types = db.query(models.DonorType.donor_type).order_by(models.DonorType.donor_type.asc()).all()
#     return donor_types
