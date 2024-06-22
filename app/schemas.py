from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class DonationHeaderBase(BaseModel):
    """
    Base model for a donation header.
    """
    donor_id: int
    donation_name: str
    donation_status: str = 'Submitted'


class MakeDonationHeader(DonationHeaderBase):
    """
    Subclass of DonationHeaderBase for creating a donation header.
    """
    pass


class DonationHeaderResponse(DonationHeaderBase):
    """
    Response model for a donation header.
    """
    date_created: datetime

    class Config:
        from_attributes = True


class DonationItemsBase(BaseModel):
    """
    Base model for donation items.
    """
    header_id: int
    item_name: str
    quantity: int
    description: str


class AddDonationItem(DonationItemsBase):
    """
    Subclass of DonationItemsBase for adding a donation item.
    """
    pass


class DonationItemResponse(DonationItemsBase):
    """
    Response model for a donation item.
    """
    id: int
    date_donated: datetime

    class Config:
        from_attributes = True


class DonationsBase(BaseModel):
    """
    Model to represent a donation item.
    """
    donation_name: str
    quantity: int
    description: str
    donation_status: str = 'Submitted'


class MakeDonation(DonationsBase):
    """
    Subclass of DonationsBase for making a donation.
    """
    pass


class DonationResponse(DonationsBase):
    """
    Response model for a donation.
    """
    id: int
    donor_id: int
    date_donated: datetime

    class Config:
        from_attributes = True


class Donor(BaseModel):
    """
    Model to represent a donor entity.
    """
    donor_name: str
    email: str
    phone_number: str
    address: str


class RegisterDonor(Donor):
    """
    Subclass of Donor for registering a donor.
    """
    pass


class DonorResponse(BaseModel):
    """
    Response model for a donor.
    """
    id: int
    email: str
    date_created: datetime

    class Config:
        from_attributes = True


class DonorCredentials(BaseModel):
    """
    Model to represent donor credentials.
    """
    username: EmailStr
    password: str
    donor_id: int


class DonorCredentialsResponse(BaseModel):
    """
    Response model for donor credentials.
    """
    donor_id: int
    username: EmailStr

    class Config:
        from_attributes = True


class DonorLogin(BaseModel):
    """
    Model for donor login.
    """
    username: EmailStr
    password: str


class ContactPerson(BaseModel):
    """
    Model to represent a contact person for a donor.
    """
    contact_name: str
    email: str
    phone_num: str


class RegisterContactPerson(ContactPerson):
    """
    Subclass of ContactPerson for registering a contact person.
    """
    pass


class ContactsResponse(ContactPerson):
    """
    Response model for a contact person.
    """
    id: int
    date_created: datetime

    class Config:
        from_attributes = True


class Employee(BaseModel):
    """
    Model to represent an employee entity.
    """
    first_name: str
    last_name: str
    email: str
    trn_number: str
    department: int
    emp_type: int
    phone_number: str


class AddEmployee(Employee):
    """
    Subclass of Employee for adding an employee.
    """
    pass


class RecipientsBase(BaseModel):
    """
    Base model to represent a recipient entity.
    """
    name: str
    email: str
    address: str
    phone_number: str
    type_id: int


class RegisterRecipient(RecipientsBase):
    """
    Subclass of RecipientsBase for registering a recipient.
    """
    pass


class RecipientResponse(BaseModel):
    """
    Response model for a recipient.
    """
    id: int
    email: str
    date_created: datetime

    class Config:
        from_attributes = True


class DonationRequestBase(BaseModel):
    """
    Base model for a donation request.
    """
    recipient_id: int
    item_name: str
    quantity: int


class MakeDonationRequest(DonationRequestBase):
    """
    Subclass of DonationRequestBase for making a donation request.
    """
    pass


class RequestResponse(DonationRequestBase):
    """
    Response model for a donation request.
    """
    id: int
    recipient_id: int
    request_date: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """
    Model to represent an authentication token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Model to represent token data.
    """
    donor_id: Optional[int] = None

