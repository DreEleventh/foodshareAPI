from fastapi import FastAPI, HTTPException, status, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body, Form
from psycopg2 import Error
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import Annotated
from sqlalchemy.orm import Session
from app import models
from app.databaseConn import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Define models for Donor and Donation
class MakeDonation(BaseModel):
    donation_name: str
    quantity: int
    description: str
    donation_status: str = 'Submitted'


class RegisterDonor(BaseModel):
    name: str
    email: str
    phone_number: str
    address: str
    type: int


class RegisterContactPerson(BaseModel):
    name: str
    email: str
    phone_number: str
    donor_id: int


class Employee(BaseModel):
    first_name: str
    last_name: str
    email: str
    trn_number: str
    department: int
    emp_type: int
    phone_number: str


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="FoodShareDB",
                                user="postgres", password="Z3ntArt#7095", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection established!!")
        break
    except Error as e:
        print(f"Could not connect. "
              f"\nError code: {e}")
        time.sleep(2)


@app.get("/sqlalchemy")
def test_postgres_db(db: Session = Depends(get_db)):
    donations = db.query(models.Donations).order_by(models.Donations.id.asc()).all()
    return {"all donations": donations}


# Make a donation endpoint
@app.post('/donations/', status_code=status.HTTP_201_CREATED)
def make_donation(donation: MakeDonation, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO donations
    # (donation_name, quantity, description, donation_status) VALUES (%s, %s, %s, %s) RETURNING *""",
    #                (donation.name, donation.quantity, donation.description, donation.status))
    # new_donation = cursor.fetchone()
    # conn.commit()
    # Adding a donation to the database user SQlAlchemy
    # new_donation = models.Donations(donation_name=donation.name, quantity=donation.quantity,
    #                                 description=donation.description, donation_status=donation.status)

    new_donation = models.Donations(**donation.dict())
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)
    return {"new donation": new_donation}


# Get all donations endpoint
@app.get("/donations/")
def get_all_donations(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM donations ORDER BY id;""")
    # donations = cursor.fetchall()
    donations = db.query(models.Donations).order_by(models.Donations.id.asc()).all()
    return {"donations": donations}


# Get a single donation by ID endpoint
@app.get("/donations/{donation_id}")
def get_donation_by_id(donation_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM donations WHERE id = %s;""", (str(donation_id),))
    # single_donation = cursor.fetchone()

    single_donation = (db.query(models.Donations).filter(models.Donations.id == donation_id)
                       .order_by(models.Donations.id.asc()).first())

    if not single_donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation with id: {donation_id} does not exist")

    return {"donation": single_donation}


# Delete a donation by ID endpoint
@app.delete("/donations/{donation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_donation(donation_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM donations WHERE id = %s RETURNING *""", (str(donation_id),))
    # remove_donation = cursor.fetchone()
    # conn.commit()

    remove_donation = db.query(models.Donations).filter(models.Donations.id == donation_id).first()

    if remove_donation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation with id {donation_id} not found")

    remove_donation.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a donation by ID endpoint
@app.put("/donations/{donation_id}")
def update_donation(donation_id: int, donation_update: MakeDonation, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE donations SET donation_name = %s, description = %s, donation_status = %s, quantity = %s
    #                   WHERE id = %s RETURNING *""",
    #                (donation_update.name, donation_update.description,
    #                donation_update.status, donation_update.quantity,
    #                 str(donation_id)))
    #
    # updated_donation = cursor.fetchone()
    # conn.commit()

    update_query = db.query(models.Donations).filter(models.Donations.id == donation_id)

    donation = update_query.first()

    if donation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Donation with id {donation_id} not found")

    update_query.update(donation_update.dict(), synchronize_session=False)
    db.commit()

    return {"message": f"Donation with id {donation_id} successfully updated"}


# Donor registration endpoint
@app.post("/donors", status_code=status.HTTP_201_CREATED)
def register_donor(donor: RegisterDonor):
    try:
        # Insert donor details into the database using parameterized query
        cursor.execute("""INSERT INTO donors (donor_name, email, phone_number, address, typeid)
                        VALUES (%s, %s, %s, %s, %s) RETURNING *""",
                       (donor.name, donor.email, donor.phone_number, donor.address, donor.type))

        # Fetch the newly created donor
        new_donor = cursor.fetchone()
        conn.commit()

        if new_donor:
            # Check if a donor was created
            return {"new donor": new_donor}
        else:
            # If no donor was created, raise an HTTPException
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed tp create donor.")

    except Exception as e:
        # If an error occurs during database operation, raise an HTTPException
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Donor display endpoint
@app.get("/donors")
def display_all_donors():
    cursor.execute("""SELECT * FROM donors ORDER BY id;""")
    donors = cursor.fetchall()
    return {"donors": donors}


# Get donor by id endpoint
@app.get("/donors/{donor_id}")
def get_donor_by_id(donor_id: int):
    cursor.execute("""SELECT * FROM donors WHERE id = %s;""", (str(donor_id),))
    single_donor = cursor.fetchone()

    if single_donor:
        return {"donor": single_donor}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation with id: {donor_id} does not exist")


# Delete a donor by ID endpoint
@app.delete("/donors/{donor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_donor_by_id(donor_id: int):
    cursor.execute("""DELETE FROM donors WHERE id = %s RETURNING *;""", (str(donor_id)))
    remove_donor = cursor.fetchone()
    conn.commit()

    if remove_donor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Donation with id: {donor_id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a donor endpoint
@app.put("/donors/{donor_id}")
def update_donor(donor_id: int, donor_update: RegisterDonor):
    cursor.execute("""UPDATE donors SET donor_name = %s, email = %s, phone_number = %s, address = %s, typeid = %s
                    WHERE id = %s RETURNING *;""", (donor_update.name, donor_update.email, donor_update.phone_number,
                                                    donor_update.address, donor_update.type, str(donor_id)))
    updated_donor = cursor.fetchone()
    conn.commit()

    if updated_donor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Donor with id: {donor_id} does not exist")

    return {"message": f"Donor with id: {donor_id} successfully updated"}


# Donor type endpoint
@app.get("/donor_type")
def get_all_donor_types():
    cursor.execute("""SELECT donor_type FROM donor_type;""")

    donor_types = cursor.fetchall()

    return donor_types


# Add donor contact endpoint
@app.post("/contacts/", status_code=status.HTTP_201_CREATED)
def register_contact(contact: RegisterContactPerson):
    cursor.execute("""INSERT INTO donor_contacts (contact_name, email, phone_num, donor_id) 
    VALUES (%s, %s, %s, %s) RETURNING *;""", (contact.name, contact.email, contact.phone_number, contact.donor_id))

    new_contact = cursor.fetchone()
    conn.commit()

    return {"new contact": new_contact}


# Get all contacts endpoint
@app.get("/contacts/")
def display_all_contacts():
    cursor.execute("SELECT * FROM donor_contacts ORDER BY id;")
    all_contacts = cursor.fetchall()
    return {"contacts": all_contacts}


# Get contact by id endpoint
@app.get("/contacts/{contact_id}")
def get_single_contact(contact_id: int):
    cursor.execute("""SELECT * FROM donor_contacts WHERE id = %s;""", (str(contact_id),))
    contact = cursor.fetchone()

    if contact:
        return {"contact": contact}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id {contact_id} not found")


# Delete contact endpoint
@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int):
    cursor.execute("""DELETE FROM donor_contacts WHERE id = %s RETURNING *;""", (str(contact_id),))
    remove_contact = cursor.fetchone()
    conn.commit()

    if remove_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact with id {contact_id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update contact person endpoint
@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact_update: RegisterContactPerson):
    cursor.execute("""UPDATE donor_contacts SET contact_name = %s, email = %s, phone_num = %s, donor_id = %s 
    WHERE id = %s RETURNING *;""", (contact_update.name, contact_update.email, contact_update.phone_number,
                                    contact_update.donor_id, str(contact_id)))

    updated_contact = cursor.fetchone()
    conn.commit()
    if updated_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact with id {contact_id} does not exist")

    return {"message": f"Contact with id {contact_id} successfully updated."}


@app.post("/employees/", status_code=status.HTTP_201_CREATED)
def create_employee(employee: Employee):
    cursor.execute("""INSERT INTO employees (first_name, last_name, email, trn_number, department_id,
     employee_type, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s)  RETURNING *""",
                   (employee.first_name, employee.last_name, employee.email, employee.trn_number,
                    employee.department, employee.emp_type, employee.phone_number))

    new_employee = cursor.fetchone()
    conn.commit()
    return {"new employee": new_employee}


@app.get("/employees/")
def display_employees():
    cursor.execute("""SELECT * FROM employees""")
    employees = cursor.fetchall()
    return {"employees": employees}


@app.get("/employees/{employee_id}/")
def get_single_employee(employee_id: int):
    cursor.execute("""SELECT * FROM employees WHERE id = %s""", (str(employee_id),))
    employee = cursor.fetchone()

    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {employee_id} not found")
    else:
        return {"employee": employee}


@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int):
    cursor.execute("""DELETE FROM employees WHERE id = %s RETURNING *""", (str(employee_id),))
    removed_employee = cursor.fetchone()
    conn.commit()

    if removed_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact with id {employee_id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee_update: Employee):
    cursor.execute("""UPDATE employees SET first_name = %s, last_name = %s, email = %s, 
    trn_number = %s, department_id = %s, employee_type = %s, phone_number = %s WHERE id = %s RETURNING *""",
                   (employee_update.first_name, employee_update.last_name, employee_update.email,
                    employee_update.trn_number, employee_update.department, employee_update.emp_type,
                    employee_update.phone_number, str(employee_id),))

    emp_update = cursor.fetchone()
    conn.commit()

    if emp_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with id {employee_id} does not exist")

    return {"message": f"Employee with id {employee_id}, successfully updated."}
