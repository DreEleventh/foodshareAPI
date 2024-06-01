from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utills
from ..databaseConn import get_db


router = APIRouter(
    prefix="/donation_request",
    tags=["Donation Request"]
)


# Donation request endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RequestResponse)
def make_request(request: schemas.MakeDonationRequest, db: Session = Depends(get_db)):
    new_request = models.DonationRequest(**request.dict())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


# Get all donation request endpoint
@router.get("/", response_model=List[schemas.RequestResponse])
def display_request(db: Session = Depends(get_db)):

    all_requests = db.query(models.DonationRequest).order_by(models.DonationRequest.id.desc()).all()

    # Convert Request objects into dictionaries
    request_dict = [request.__dict__ for request in all_requests]

    return request_dict


# Get a single donation request by id endpoint
@router.get("/{request_id}")
def get_request_by_id(request_id: int, db: Session = Depends(get_db)):
    get_request = (db.query(models.DonationRequest).filter(models.DonationRequest.id == request_id)
                   .order_by(models.DonationRequest.id.asc()).first())

    if not get_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Request with the id {request_id} does not exist")

    return get_request


@router.delete("/{request_id}")
def delete_request(request_id: int, db: Session = Depends(get_db)):
    remove_request = db.query(models.DonationRequest).filter(models.DonationRequest.id == request_id).first()

    if remove_request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Request with id {request_id} does not exist.")

    db.delete(remove_request)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{request_id}")
def update_request(request_id: int, request_update: schemas.MakeDonationRequest, db: Session = Depends(get_db)):
    update_query = db.query(models.DonationRequest).filter(models.DonationRequest.id == request_id)

    request = update_query.first()

    if request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Request with is {request_id} does not exist.")

    update_query.update(request_update.dict(), synchronize_session=False)
    db.commit()

    return {"message": f"Request successfully updated."}
