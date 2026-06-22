from fastapi import HTTPException


def validate_booking(
    start_time,
    end_time
):

    if end_time <= start_time:

        raise HTTPException(
            status_code=400,
            detail="End time must be greater than start time")
