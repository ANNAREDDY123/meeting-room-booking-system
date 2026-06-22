from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.booking import Booking
from models.employee import Employee
from models.room import Room
from models.participant import Participant

from schemas.booking import BookingCreate
from schemas.participant import ParticipantCreate

from services.booking_service import validate_booking

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def send_reminder():
    print("Meeting reminder sent")


@router.post("/")
def create_booking(
    booking: BookingCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    validate_booking(
        booking.start_time,
        booking.end_time
    )

    employee = db.query(Employee).filter(
        Employee.id == booking.employee_id
    ).first()

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    room = db.query(Room).filter(
        Room.id == booking.room_id
    ).first()

    if not room:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    if not room.is_available:

        raise HTTPException(
            status_code=400,
            detail="Room unavailable"
        )

    existing_room_booking = db.query(Booking).filter(
        Booking.room_id == booking.room_id
    ).first()

    if existing_room_booking:

        raise HTTPException(
            status_code=400,
            detail="Room already booked"
        )

    existing_employee_booking = db.query(Booking).filter(
        Booking.employee_id == booking.employee_id
    ).first()

    if existing_employee_booking:

        raise HTTPException(
            status_code=400,
            detail="Employee already has meeting"
        )

    new_booking = Booking(
        employee_id=booking.employee_id,
        room_id=booking.room_id,
        meeting_title=booking.meeting_title,
        start_time=booking.start_time,
        end_time=booking.end_time
    )

    db.add(new_booking)

    db.commit()

    db.refresh(new_booking)

    background_tasks.add_task(
        send_reminder
    )

    return new_booking


@router.get("/")
def get_bookings(
    date: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Booking)

    total_records = query.count()

    total_pages = (
        total_records + limit - 1
    ) // limit

    bookings = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total_records,
        "current_page": page,
        "total_pages": total_pages,
        "data": bookings
    }


@router.get("/{booking_id}")
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return booking


@router.delete("/{booking_id}")
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    db.delete(booking)

    db.commit()

    return {
        "message":
        "Booking deleted"
    }


@router.post("/{booking_id}/participants")
def add_participant(
    booking_id: int,
    participant: ParticipantCreate,
    db: Session = Depends(get_db)
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    room = db.query(Room).filter(
        Room.id == booking.room_id
    ).first()

    count = db.query(Participant).filter(
        Participant.booking_id == booking_id
    ).count()

    if count >= room.capacity:

        raise HTTPException(
            status_code=400,
            detail="Room capacity exceeded"
        )

    new_participant = Participant(
        booking_id=booking_id,
        employee_name=participant.employee_name
    )

    db.add(new_participant)

    db.commit()

    return {
        "message":
        "Participant added"
    }


@router.get("/{booking_id}/participants")
def get_participants(
    booking_id: int,
    db: Session = Depends(get_db)
):

    return db.query(Participant).filter(
        Participant.booking_id == booking_id
    ).all()
