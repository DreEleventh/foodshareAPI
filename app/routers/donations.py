from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .. import models, schemas, utills, oauth2, notify
from ..databaseConn import get_db

router = APIRouter(
    prefix="/donations",
    tags=["Donations"],
)


# Make a donation endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DonationResponse)
def make_donation(donation: schemas.MakeDonation, db: Session = Depends(get_db),
                  current_donor: models.Donors = Depends(oauth2.get_current_user)):
    """
    Endpoint to make a new donation.
    """

    new_donation = models.Donations(donor_id=current_donor.id, **donation.dict())
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)

    # Update the donor's total_donations
    donor = db.query(models.Donors).filter(models.Donors.id == current_donor.id).first()
    if donor:
        donor.total_donations = (donor.total_donations or 0) + 1
        db.commit()

    return new_donation


# get all donations for a specific user
@router.get("/user", response_model=List[schemas.DonationResponse])
def fetch_user_donations(db: Session = Depends(get_db),
                         current_donor: models.Donors = Depends(oauth2.get_current_user)):
    """
    Endpoint to get all donations for a specific.
    """
    donations = (db.query(models.Donations).filter(models.Donations.donor_id == current_donor.id)
                 .order_by(models.Donations.id.desc()).all())

    # Convert Donations objects into dictionaries
    donation_dicts = [donation.__dict__ for donation in donations]

    return donation_dicts


@router.get("/user/submitted", response_model=List[schemas.DonationResponse])
def fetch_submitted_donations(db: Session = Depends(get_db),
                              current_donor: models.Donors = Depends(oauth2.get_current_user)):
    """
    Endpoint to get all donations for a specific user where the status is 'Submitted'.
    """
    donations = (db.query(models.Donations).filter(and_(models.Donations.donor_id == current_donor.id,
                                                        models.Donations.donation_status == 'Submitted')).order_by(
        models.Donations.id.desc()).all())

    # Convert Donations objects into dictionaries
    donation_dicts = [donation.__dict__ for donation in donations]

    return donation_dicts


# Get all donations endpoint
@router.get("/all", response_model=List[schemas.DonationResponse])
def get_all_donations(db: Session = Depends(get_db)):
    """
    Endpoint to get all donations.
    """
    donations = db.query(models.Donations).order_by(models.Donations.id.desc()).all()

    # Convert Donations objects into dictionaries
    donation_dicts = [donation.__dict__ for donation in donations]

    return donation_dicts


# Get all posted  donations
@router.get("/all/posted", response_model=List[schemas.DonationResponse])
def get_all_posted_donations(db: Session = Depends(get_db)):
    donation_query = db.query(models.Donations).filter(and_(models.Donations.donation_status == 'Posted')).order_by(
        models.Donations.id.desc()).all()

    donation_dict = [donations.__dict__ for donations in donation_query]

    return donation_dict


# Get a single donation by ID endpoint for particular user
@router.get("/user/{donation_id}")
def fetch_single_donation(donation_id: int, db: Session = Depends(get_db),
                          current_donor: models.Donors = Depends(oauth2.get_current_user)):
    """
    Endpoint to get a single donation by its ID for a particular user
    """
    single_donation = (db.query(models.Donations).filter(models.Donations.id == donation_id)
                       .order_by(models.Donations.id.asc()).first())

    if not single_donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation with id: {donation_id} does not exist")

    if single_donation.donor_id != current_donor.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    return {"donation": single_donation}


# Get a single donation by ID endpoint
@router.get("/single/{donation_id}")
def get_donation_by_id(donation_id: int, db: Session = Depends(get_db),
                       current_donor: int = Depends(oauth2.get_current_user)):
    """
    Endpoint to get a single donation by its ID.
    """
    single_donation = (db.query(models.Donations).filter(models.Donations.id == donation_id)
                       .order_by(models.Donations.id.asc()).first())

    if not single_donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation with id: {donation_id} does not exist")

    return {"donation": single_donation}


# Donation pickup endpoint
@router.put("/pickup/{donation_id}")
def pickup_donation(donation_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to pick up a donation by updating its status to 'posted'.
    """

    # Retrieve the donation from the database by its ID
    update_query = db.query(models.Donations).filter(models.Donations.id == donation_id)

    donation = update_query.first()

    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation with id: {donation_id} does not exist.")

    # Update the status of the donation
    donation.donation_status = 'Picked'
    db.commit()
    db.refresh(donation)

    return {"message": f"Donation with id {donation_id} successfully updated"}


# Donation post endpoint
@router.put("/post/{donation_id}")
def post_donation(donation_id: int, db: Session = Depends(get_db)):
    update_query = db.query(models.Donations).filter(models.Donations.id == donation_id)

    donation = update_query.first()

    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation with id: {donation_id} does not exist.")

    donation.donation_status = "Posted"
    db.commit()
    db.refresh(donation)
    return {"message": f"Donation with id {donation_id} successfully updated"}


# Delete a donation by ID endpoint
@router.delete("/{donation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_donation(donation_id: int, db: Session = Depends(get_db),
                    current_donor: models.Donors = Depends(oauth2.get_current_user)):
    """
    Endpoint to delete a donation by its ID.
    """
    donation_query = db.query(models.Donations).filter(models.Donations.id == donation_id)

    remove_donation = donation_query.first()

    if remove_donation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation with id {donation_id} not found")

    if remove_donation.donor_id != current_donor.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    db.delete(remove_donation)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a donation by ID endpoint
@router.put("/{donation_id}")
def update_donation(donation_id: int, donation_update: schemas.MakeDonation, db: Session = Depends(get_db),
                    current_donor: models.Donors = Depends(oauth2.get_current_user)):
    """
    Endpoint to update a donation by its ID.
    """
    update_query = db.query(models.Donations).filter(models.Donations.id == donation_id)

    donation = update_query.first()

    if donation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Donation with id {donation_id} not found.")

    if donation.donor_id != current_donor.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    update_query.update(donation_update.dict(), synchronize_session=False)
    db.commit()

    return {"message": f"Donation with id {donation_id} successfully updated"}
