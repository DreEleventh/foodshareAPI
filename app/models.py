from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .databaseConn import Base


class Donations(Base):
    __tablename__ = 'donations'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    donation_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    donation_status = Column(String, nullable=False)
    date_donated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class DonationStatus(Base):
    __tablename__ = 'donation_statuses'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    status = Column(String, nullable=False)


class Donors(Base):
    __tablename__ = 'donors'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    donor_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey("donor_type.id", ondelete="CASCADE"), nullable=False)
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    total_donations = Column(Integer)

    type = relationship("DonorType")


class DonorCredentials(Base):
    __tablename__ = 'donor_credentials'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    last_login = Column(TIMESTAMP(timezone=True))
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    donor_id = Column(Integer, ForeignKey('donors.id', ondelete="CASCADE"), nullable=False)

    donor = relationship("Donors")


class DonorContacts(Base):
    __tablename__ = 'donor_contacts'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    contact_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_num = Column(String, nullable=False)
    donor_id = Column(Integer, ForeignKey("donors.id", ondelete="CASCADE"), nullable=False)
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    donor = relationship("Donors")


class DonorType(Base):
    __tablename__ = 'donor_type'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    donor_type = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False, unique=True)



