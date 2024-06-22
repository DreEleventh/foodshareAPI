from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utills, oauth2
from ..databaseConn import get_db

router = APIRouter(
    prefix="/contacts",
    tags=['Donor Contacts'],
)


# Add donor contact endpoint
@router.post("/", status_code=status.HTTP_201_CREATED)
def register_contact(contact: schemas.RegisterContactPerson, db: Session = Depends(get_db),
                     current_donor: models.Donors = Depends(oauth2.get_current_user)):
    """
    Endpoint to register a new contact person.
    """
    new_contact = models.DonorContacts(donor_id=current_donor.id, **contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact


# Endpoint that returns all contact for a particular user
@router.get("/user", response_model=List[schemas.ContactsResponse])
def fetch_donor_contacts(db: Session = Depends(get_db),
                         current_donor: models.Donors = Depends(oauth2.get_current_user)):
    """
    Endpoint to get all contact persons for a particular donor.
    """
    all_contacts = (db.query(models.DonorContacts).filter(models.DonorContacts.donor_id == current_donor.id)
                    .order_by(models.DonorContacts.id.asc()).all())

    return all_contacts


# Get all contacts endpoint
@router.get("/all", response_model=List[schemas.ContactsResponse])
def display_all_contacts(db: Session = Depends(get_db)):
    """
    Endpoint to get all contact persons.
    """
    all_contacts = db.query(models.DonorContacts).order_by(models.DonorContacts.id.asc()).all()
    return all_contacts


# Get contact by id endpoint
@router.get("/user/{contact_id}")
def fetch_single_contact(contact_id: int, db: Session = Depends(get_db),
                         current_donor: models.Donors = Depends(oauth2.get_current_user)):
    """
    Endpoint to get a contact person by its ID.
    """
    contact = db.query(models.DonorContacts).filter(models.DonorContacts.id == contact_id).order_by(
        models.DonorContacts.id.asc()).first()

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact with id: {contact_id} does not exist")

    if contact.donor_id != current_donor.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")

    return {"contact": contact}


# Get contact by id endpoint
@router.get("single/{contact_id}")
def get_single_contacts(contact_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get a contact person by its ID.
    """
    contact = db.query(models.DonorContacts).filter(models.DonorContacts.id == contact_id).order_by(
        models.DonorContacts.id.asc()).first()

    if contact:
        return {"contact": contact}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id {contact_id} not found")


# Delete contact endpoint
@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db),
                   current_donor: models.Donors = Depends(oauth2.get_current_user)):
    """
    Endpoint to delete a contact person by its ID.
    """
    remove_query = db.query(models.DonorContacts).filter(models.DonorContacts.id == contact_id)

    remove_contact = remove_query.first()

    if remove_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact with id {contact_id} does not exist")

    if remove_contact.donor_id != current_donor.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action.")

    db.delete(remove_contact)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update contact person endpoint
@router.put("/{contact_id}")
def update_contact(contact_id: int, contact_update: schemas.RegisterContactPerson, db: Session = Depends(get_db),
                   current_donor: models.Donors = Depends(oauth2.get_current_user)):
    """
    Endpoint to update a contact person by its ID.
    """
    update_query = db.query(models.DonorContacts).filter(models.DonorContacts.id == contact_id)

    contact = update_query.first()

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact with id {contact_id} does not exist")

    if contact.donor_id != current_donor.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    update_query.update(contact_update.dict(), synchronize_session=False)
    db.commit()

    return {"message": f"Contact with id {contact_id} successfully updated."}
