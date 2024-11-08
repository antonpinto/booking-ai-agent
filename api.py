from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Booking(BaseModel):
    location: str
    date: str
    person: str
    desk: str = None


desks = ["D001", "D002", "D003", "D004"]
bookings = [
    Booking(
        location="Lisbon", date="2024-12-01", person="John Doe", desk=desks[0]
    )
]
app = FastAPI()


@app.post("/bookings/", response_model=Booking)
def create_booking(booking: Booking):
    existing_reserve = [
        b for b in bookings if b.date == booking.date and b.person == booking.person
    ]
    if len(existing_reserve) == 1:
        return existing_reserve[0]

    reserved_desks = [b.desk for b in bookings if b.date == booking.date]
    free_desks = [d for d in desks if d not in reserved_desks]

    if len(free_desks) == 0:
        raise HTTPException(status_code=400, detail="No free desks!")

    booking.desk = free_desks[0]
    bookings.append(booking)
    return booking


@app.get("/bookings/", response_model=List[Booking])
def get_bookings(date: str = None, location: str = "Lisbon"):
    return [b for b in bookings if (b.date == date or date is None) and b.location == location]


@app.get("/requesters/", response_model=List[str])
def get_booking_requesters(date: str, location: str = "Lisbon"):
    return [b.person for b in bookings if b.date == date and b.location == location]
