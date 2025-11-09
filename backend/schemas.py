from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class Venue(BaseModel):
    name: str
    location: Optional[str] = None
    capacity: Optional[int] = None

class Client(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None

class Booking(BaseModel):
    date: date
    time: Optional[str] = None
    client: str
    venue: str
    guests: Optional[int] = None
    status: str = Field(default="Inquiry")

class Expense(BaseModel):
    date: date
    category: str
    amount: float
    description: Optional[str] = None

class User(BaseModel):
    email: str
    name: Optional[str] = None
    role: str = Field(default="owner")

class ListResponse(BaseModel):
    items: List[dict]
    count: int
    timestamp: datetime
