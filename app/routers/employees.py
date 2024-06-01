from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utills
from ..databaseConn import get_db

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


# Create employee endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, operation_id="create_employee")
def create_employee(employee: schemas.AddEmployee, db: Session = Depends(get_db)):
    """
    Endpoint to create a new employee.
    """
    new_employee = models.Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


# Get all employees endpoint
@router.get("/")
def display_employees(db: Session = Depends(get_db)):
    """
    Endpoint to get all employees.
    """
    all_employees = db.query(models.Employee).order_by(models.Employee.id.asc()).all()
    return all_employees


# Get single employee by ID endpoint
@router.get("/{employee_id}/")
def get_single_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get a single employee by its ID.
    """
    employee = (db.query(models.Employee).filter(models.Employee.id == employee_id)
                .order_by(models.Employee.id.asc()).first())

    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {employee_id} not found")
    else:
        return {"employee": employee}


# Delete employee by ID endpoint
@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete an employee by its ID.
    """
    removed_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    if removed_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with id {employee_id} does not exist")

    removed_employee.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update employee by ID endpoint
@router.put("/{employee_id}")
def update_employee(employee_id: int, employee_update: schemas.AddEmployee, db: Session = Depends(get_db)):
    """
    Endpoint to update an employee by its ID.
    """
    update_query = db.query(models.Employee).filter(models.Employee.id == employee_id)

    employee = employee_update

    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with id {employee_id} does not exist")

    update_query.update(employee_update, synchronize_session=False)
    db.commit()

    return {"message": f"Employee with id {employee_id}, successfully updated."}
