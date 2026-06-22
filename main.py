from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import (
    Base,
    engine
)

from models.user import User
from models.employee import Employee
from models.room import Room
from models.booking import Booking
from models.participant import Participant

from routes.auth import router as auth_router
from routes.employees import router as employee_router
from routes.rooms import router as room_router
from routes.bookings import router as booking_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Meeting Room Booking System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(room_router)
app.include_router(booking_router)


@app.get("/")
def home():

    return {
        "message":
        "Meeting Room Booking System"
    }
