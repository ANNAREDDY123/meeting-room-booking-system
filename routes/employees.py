from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.employee import Employee

from schemas.employee import EmployeeCreate

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        role=employee.role
    )

    db.add(new_employee)

    db.commit()

    db.refresh(new_employee)

    return new_employee


@router.get("/")
def get_employees(
    department: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(Employee)

    if department:

        query = query.filter(
            Employee.department == department
        )

    return query.all()


@router.get("/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


@router.put("/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    db_employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not db_employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db_employee.name = employee.name
    db_employee.email = employee.email
    db_employee.department = employee.department
    db_employee.role = employee.role

    db.commit()

    return {
        "message":
        "Employee updated"
    }
