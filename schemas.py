"""
Database Schemas for VenueOS

Each Pydantic model below represents a MongoDB collection used by the app.
Collection name is the lowercase class name (e.g., Booking -> "booking").
"""

from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class Venue(BaseModel):
    """Venues managed in the system"""
    name: str = Field(..., description="Venue name")
    location: str = Field(..., description="Address or general location")
    capacity: Optional[int] = Field(None, ge=0, description="Max guest capacity")
    spaces: List[str] = Field(default_factory=list, description="Spaces/rooms e.g. Ballroom, Garden")
    contact_email: Optional[EmailStr] = Field(None, description="Venue contact email")
    contact_phone: Optional[str] = Field(None, description="Venue contact phone")


class Client(BaseModel):
    """Clients booking events (couples, companies, etc.)"""
    name: str = Field(..., description="Primary contact or couple names")
    email: Optional[EmailStr] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone")
    company: Optional[str] = Field(None, description="Company (for corporate events)")
    notes: Optional[str] = Field(None, description="Internal notes")


class Booking(BaseModel):
    """Event bookings at the venue"""
    title: str = Field(..., description="Event title e.g., 'Singh Wedding'")
    client_id: Optional[str] = Field(None, description="Reference to client _id as string")
    venue_id: Optional[str] = Field(None, description="Reference to venue _id as string")
    space: Optional[str] = Field(None, description="Specific room/space used")
    date: datetime = Field(..., description="Event start date/time")
    end_date: Optional[datetime] = Field(None, description="Event end date/time")
    guests: Optional[int] = Field(None, ge=0, description="Expected guest count")
    status: str = Field("tentative", description="tentative | confirmed | cancelled")
    estimated_revenue: Optional[float] = Field(None, ge=0, description="Expected revenue for this booking")


class Expense(BaseModel):
    """Operational expenses tied to a booking or general ops"""
    category: str = Field(..., description="Category e.g., catering, staff, decor, rental")
    amount: float = Field(..., ge=0, description="Expense amount")
    booking_id: Optional[str] = Field(None, description="Related booking _id as string")
    notes: Optional[str] = Field(None, description="Details about the expense")
    date: datetime = Field(default_factory=datetime.utcnow, description="When the expense occurred")


# Minimal user schema for admins/teammates (optional for later use)
class User(BaseModel):
    name: str
    email: EmailStr
    role: str = Field("manager", description="manager | staff | owner")
    is_active: bool = True
