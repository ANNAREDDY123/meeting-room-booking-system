from pydantic import BaseModel


class RoomCreate(BaseModel):

    room_name: str

    capacity: int

    location: str

    is_available: bool = True
