from pydantic import BaseModel


class ParticipantCreate(BaseModel):

    employee_name: str
