from pydantic import BaseModel

from datetime import datetime


class BookingCreate(BaseModel):

    employee_id: int

    room_id: int

    meeting_title: str

    start_time: datetime

    end_time: datetime
