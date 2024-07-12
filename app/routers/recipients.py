from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utills, oauth2_recipients
from ..databaseConn import get_db

router = APIRouter(
    prefix="/recipients",
    tags=["Recipients"]
)


# Register Recipient endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RecipientResponse)
def register_recipient(recipient: schemas.RegisterRecipient, db: Session = Depends(get_db)):

    try:

        new_recipient = models.Recipients(**recipient.dict())
        db.add(new_recipient)
        db.commit()
        db.refresh(new_recipient)

        if new_recipient:
            return new_recipient
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Failed to create recipient.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Get all recipients endpoints
@router.get("/")
def get_all_recipients(db: Session = Depends(get_db)):
    recipients = db.query(models.Recipients).order_by(models.Recipients.id.asc()).all()
    return recipients


# Get the current logged in recipient
@router.get("/current_recipient/")
def fetch_current_recipient(db: Session = Depends(get_db),
                            current_recipient: models.Recipients = Depends(oauth2_recipients.get_current_recipient)):

    fetch_recipient = db.query(models.Recipients).filter(
        models.Recipients.id == current_recipient.id).order_by(models.Recipients.id.asc()).first()

    if fetch_recipient.id != current_recipient.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action.")

    return fetch_recipient


# Get recipient by id
@router.get("/{recipient_id}")
def get_recipient_by_id(recipient_id: int, db: Session = Depends(get_db)):
    single_recipient = (db.query(models.Recipients).filter(models.Recipients.id == recipient_id)
                        .order_by(models.Recipients.id.asc()).first())

    if single_recipient:
        return single_recipient
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Recipient with id {recipient_id} does not exit.")


# Delete a recipient by id
@router.delete("/{recipient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipient_by_id(recipient_id: int, db: Session = Depends(get_db)):
    delete_recipient = db.query(models.Recipients).filter(models.Recipients.id == recipient_id).first()

    if delete_recipient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Recipient with id {recipient_id} does not exist.")

    db.delete(delete_recipient)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update recipient end point
@router.put("/{recipient_id}")
def update_recipient(recipient_id: int, recipient_update: schemas.RegisterRecipient, db: Session = Depends(get_db)):
    update_query  = db.query(models.Recipients).filter(models.Recipients.id == recipient_id)

    recipient = update_query.first()

    if recipient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Recipient with id {recipient_id} does not exist.")

    update_query.update(recipient_update.dict(), synchronize_session=False)
    db.commit()

    return {"message": f"Recipient with id {recipient_id} successfully updated."}

