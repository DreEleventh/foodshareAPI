from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .. import models, schemas, utills, oauth2_recipients
from ..databaseConn import get_db


router = APIRouter(
    prefix="/donation_request",
    tags=["Donation Request"]
)


# Donation request endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RequestResponse)
def make_request(request: schemas.MakeDonationRequest, db: Session = Depends(get_db),
                 current_recipient: models.Recipients = Depends(oauth2_recipients.get_current_recipient)):

    new_request = models.DonationRequest(recipient_id=current_recipient.id, **request.dict())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


# Get all request for a particular user
@router.get("/user", response_model=List[schemas.RequestResponse])
def fetch_user_request(db: Session = Depends(get_db),
                       current_recipient: models.Recipients = Depends(oauth2_recipients.get_current_recipient)):

    all_requests = (db.query(models.DonationRequest).filter(models.DonationRequest.recipient_id == current_recipient.id)
                    .order_by(models.DonationRequest.id.desc()).all())

    # Convert Request objects into dictionaries
    request_dict = [request.__dict__ for request in all_requests]

    return request_dict


# Get all donation request endpoint
@router.get("/all", response_model=List[schemas.RequestResponse])
def display_request(db: Session = Depends(get_db)):

    all_requests = db.query(models.DonationRequest).order_by(models.DonationRequest.id.desc()).all()

    # Convert Request objects into dictionaries
    request_dict = [request.__dict__ for request in all_requests]

    return request_dict


# Get a single donation by id for a particular recipient
@router.get("/user/{request_id}")
def fetch_single_request(request_id: int, db: Session = Depends(get_db),
                         current_recipient: models.Recipients = Depends(oauth2_recipients.get_current_recipient)):

    request = (db.query(models.DonationRequest).filter(models.DonationRequest.id == request_id)
               .order_by(models.DonationRequest.id.asc()).first())

    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation Request with id {request_id} does not exist.")

    if request.recipient_id != current_recipient.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    return request


# Get a single donation request by id endpoint
@router.get("/single/{request_id}")
def get_request_by_id(request_id: int, db: Session = Depends(get_db)):
    get_request = (db.query(models.DonationRequest).filter(models.DonationRequest.id == request_id)
                   .order_by(models.DonationRequest.id.asc()).first())

    if not get_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Request with the id {request_id} does not exist")

    return get_request


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(request_id: int, db: Session = Depends(get_db),
                   current_recipient: models.Recipients = Depends(oauth2_recipients.get_current_recipient)):

    request_query = db.query(models.DonationRequest).filter(models.DonationRequest.id == request_id)

    remove_request = request_query.first()

    if remove_request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Request with id {request_id} does not exist.")

    if remove_request.recipient_id != current_recipient.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    db.delete(remove_request)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{request_id}")
def update_request(request_id: int, request_update: schemas.MakeDonationRequest, db: Session = Depends(get_db),
                   current_recipient: models.Recipients = Depends(oauth2_recipients.get_current_recipient)):

    update_query = db.query(models.DonationRequest).filter(models.DonationRequest.id == request_id)

    request = update_query.first()

    if request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Request with is {request_id} does not exist.")

    if request.recipient_id != current_recipient.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    update_query.update(request_update.dict(), synchronize_session=False)
    db.commit()

    return {"message": f"Request successfully updated."}
