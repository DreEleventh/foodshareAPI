from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session

from .. import models, schemas, utills
from ..databaseConn import get_db


router = APIRouter(
    prefix="/donation_items",
    tags=['Donation Items']
)


# Donation items endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DonationItemResponse)
def add_donation_item(donation_item: schemas.AddDonationItem, db : Session = Depends(get_db)):

    new_donation_item = models.DonationItems(**donation_item.dict())

    db.add(new_donation_item)
    db.commit()
    db.refresh(new_donation_item)

    return new_donation_item


# Get all donation items
@router.get("/", response_model=List[schemas.DonationItemResponse])
def get_all_donation_items(db: Session = Depends(get_db)):

    donation_items = db.query(models.DonationItems).order_by(models.DonationItems.id.desc()).all()

    donation_items_dict = [items.__dict__ for items in donation_items]

    return donation_items_dict


# Get a single donation item
@router.get("/{item_id}")
def get_item_by_it(item_id: int, db: Session = Depends(get_db)):
    single_item = (db.query(models.DonationItems).filter(models.DonationItems.id == item_id)
                   .order_by(models.DonationItems.id.desc()).first())

    if not single_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation item with id {item_id} does not exist.")

    return single_item


# Delete a donation item via id
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_donation_header(item_id: int, db: Session = Depends(get_db)):
    remove_item = db.query(models.DonationItems).filter(models.DonationItems.id == item_id).first()

    if remove_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The item with id {item_id} not found")

    db.delete(remove_item)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a donation item via its id
@router.put("/{item_id}")
def update_donation_item(item_id: int, item_update: schemas.AddDonationItem, db: Session = Depends(get_db)):
    update_query = db.query(models.DonationItems).filter(models.DonationItems.id == item_id)

    items = update_query.first()

    if items is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Donation item with id {item_id} not found.")

    update_query.update(item_update.dict(), synchronize_session=False)
    db.commit()

    return {"message": f"Donation item with id {item_id} successfully updated."}

