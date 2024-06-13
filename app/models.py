from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .databaseConn import Base


class DonationHeader(Base):
    """
    Model for the 'donations_header' table.
    Represents the header information for a donation.
    """
    __tablename__ = 'donations_header'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    donor_id = Column(Integer, ForeignKey('donors.id', ondelete="CASCADE"), nullable=False)
    donation_name = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False)
    donation_status = Column(String, nullable=False)
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    donor = relationship("Donors")


class DonationItems(Base):
    """
    Model for the 'donation_items' table.
    Represents individual items within a donation.
    """
    __tablename__ = 'donation_items'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    header_id = Column(Integer, ForeignKey('donations_header.id', ondelete="CASCADE"), nullable=False)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    date_donated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    donations_header = relationship("DonationHeader")


class Donations(Base):
    """
    Model for the 'donations' table.
    Represents a donation.
    """
    __tablename__ = 'donations'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    donation_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    donation_status = Column(String, nullable=False)
    date_donated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    donor_id = Column(Integer, ForeignKey('donors.id', ondelete="CASCADE"), nullable=False)

    donor = relationship("Donors")


class DonationStatus(Base):
    """
    Model for the 'donation_statuses' table.
    Represents the status of a donation.
    """
    __tablename__ = 'donation_statuses'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    status = Column(String, nullable=False)


class Donors(Base):
    """
    Model for the 'donors' table.
    Represents a donor.
    """
    __tablename__ = 'donors'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    donor_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    total_donations = Column(Integer)
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class DonorCredentials(Base):
    """
    Model for the 'donor_credentials' table.
    Represents donor credentials.
    """
    __tablename__ = 'donor_credentials'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    last_login_time = Column(TIMESTAMP(timezone=True))
    donor_id = Column(Integer, ForeignKey('donors.id', ondelete="CASCADE"), nullable=False)

    donor = relationship("Donors")


class DonorContacts(Base):
    """
    Model for the 'donor_contacts' table.
    Represents contacts for a donor.
    """
    __tablename__ = 'donor_contacts'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    contact_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_num = Column(String, nullable=False)
    donor_id = Column(Integer, ForeignKey("donors.id", ondelete="CASCADE"), nullable=False)
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    donor = relationship("Donors")


class DonorType(Base):
    """
    Model for the 'donor_type' table.
    Represents types of donors.
    """
    __tablename__ = 'donor_type'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    donor_type = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False, unique=True)


class Employee(Base):
    """
    Model for the 'employees' table.
    Represents an employee.
    """
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    trn_number = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("employee_departments.id", onupdate="CASCADE"), nullable=False)
    employee_type = Column(Integer, ForeignKey("employee_types.id", onupdate="CASCADE"), nullable=False)
    date_employed = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class EmployeeType(Base):
    """
    Model for the 'employee_types' table.
    Represents types of employees.
    """
    __tablename__ = 'employee_types'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    emp_type = Column(String, nullable=False)


class EmployeeDepartment(Base):
    """
    Model for the 'employee_departments' table.
    Represents departments of employees.
    """
    __tablename__ = 'employee_departments'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    department_name = Column(String, nullable=False)


class EmployeeCredentials(Base):
    """
    Model for the 'employee_credentials' table.
    Represents credentials of employees.
    """
    __tablename__ = 'employee_credentials'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String)
    last_login_time = Column(TIMESTAMP(timezone=True), nullable=False)


class EmployeeDriversLicenses(Base):
    """
    Model for the 'employee_drivers_licenses' table.
    Represents drivers' licenses of employees.
    """
    __tablename__ = 'employee_drivers_licenses'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    license_number = Column(String, nullable=False, unique=True)
    expiration_date = Column(Date, nullable=False)
    license_type = Column(String, nullable=False)


class Recipients(Base):
    """
    Model for the 'recipients' table.
    Represents recipients.
    """
    __tablename__ = 'recipients'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey("recipient_types.id", onupdate="CASCADE"), nullable=False)
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    recipient_type = relationship("RecipientType")


class RecipientCredentials(Base):
    """
    Model for the 'recipient_credentials' table.
    Represents credentials of recipients.
    """
    __tablename__ = 'recipient_credentials'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipient_id = Column(Integer, ForeignKey("recipients.id", ondelete="CASCADE"), nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String)
    last_login_time = Column(TIMESTAMP(timezone=True), nullable=False)

    recipients = relationship("Recipients")


class RecipientType(Base):
    """
    Model for the 'recipient_types' table.
    Represents types of recipients.
    """
    __tablename__ = 'recipient_types'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipient_type = Column(String, nullable=False, unique=True)


class DonationRequest(Base):
    """
    Model for the 'donation_requests' table.
    Represents donation requests from recipients.
    """
    __tablename__ = 'donation_requests'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipient_id = Column(Integer, ForeignKey('recipients.id', ondelete='CASCADE'), nullable=False)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    request_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    recipients = relationship("Recipients")


class DonationPickUp(Base):
    """
    Model for the 'donation_pickup' table.
    Represents the pickup of donations.
    """
    __tablename__ = 'donation_pickup'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipient_id = Column(Integer, ForeignKey("recipients.id", ondelete="CASCADE"), nullable=False)
    donation_id = Column(Integer, ForeignKey("donations.id", ondelete="CASCADE"), nullable=False)
    time_picked = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    recipients = relationship("Recipients")
    donations = relationship("Donations")

