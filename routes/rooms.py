from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.room import Room

from schemas.room import RoomCreate

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db)
):

    new_room = Room(
        room_name=room.room_name,
        capacity=room.capacity,
        location=room.location,
        is_available=room.is_available
    )

    db.add(new_room)

    db.commit()

    db.refresh(new_room)

    return new_room


@router.get("/")
def get_rooms(
    capacity: int = None,
    db: Session = Depends(get_db)
):

    query = db.query(Room)

    if capacity:

        query = query.filter(
            Room.capacity >= capacity
        )

    return query.all()


@router.get("/{room_id}")
def get_room(
    room_id: int,
    db: Session = Depends(get_db)
):

    room = db.query(Room).filter(
        Room.id == room_id
    ).first()

    if not room:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    return room


@router.put("/{room_id}")
def update_room(
    room_id: int,
    room: RoomCreate,
    db: Session = Depends(get_db)
):

    db_room = db.query(Room).filter(
        Room.id == room_id
    ).first()

    if not db_room:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    db_room.room_name = room.room_name
    db_room.capacity = room.capacity
    db_room.location = room.location
    db_room.is_available = room.is_available

    db.commit()

    return {
        "message":
        "Room updated"
    }
