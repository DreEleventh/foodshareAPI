import hashlib
import time
import psycopg2
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from app import models, schemas, utills
from app.databaseConn import engine, get_db
from app.routers import (donations, donors, donor_contacts, donor_credentials, employees,
                         recipients, recipient_credentials, donation_request, donation_header, donation_items, auth)

# Create database tables based on models
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Configure CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(donations.router)
app.include_router(donors.router)
app.include_router(donor_contacts.router)
app.include_router(donor_credentials.router)
app.include_router(employees.router)
app.include_router(employees.router)
app.include_router(recipients.router)
app.include_router(recipient_credentials.router)
app.include_router(donation_request.router)
app.include_router(donation_header.router)
app.include_router(donation_items.router)

app.include_router(auth.router)