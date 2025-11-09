from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime
from schemas import Venue, Client, Booking, Expense, ListResponse
from database import create_document, get_documents, get_db

app = FastAPI(title="VenueOS API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
def test():
    db = get_db()
    try:
        names = db.list_collection_names()
    except Exception as e:
        names = [f"error: {e}"]
    return {
        "status": "ok",
        "time": datetime.utcnow().isoformat(),
        "collections": names,
    }

# Venues
@app.post("/venues")
def create_venue(venue: Venue):
    doc = create_document("venue", venue)
    return doc

@app.get("/venues", response_model=ListResponse)
async def list_venues(limit: Optional[int] = 100):
    items = get_documents("venue", {}, limit)
    return {"items": items, "count": len(items), "timestamp": datetime.utcnow()}

# Clients
@app.post("/clients")
def create_client(client: Client):
    doc = create_document("client", client)
    return doc

@app.get("/clients", response_model=ListResponse)
async def list_clients(limit: Optional[int] = 100):
    items = get_documents("client", {}, limit)
    return {"items": items, "count": len(items), "timestamp": datetime.utcnow()}

# Bookings
@app.post("/bookings")
def create_booking(booking: Booking):
    doc = create_document("booking", booking)
    return doc

@app.get("/bookings", response_model=ListResponse)
async def list_bookings(limit: Optional[int] = 100):
    items = get_documents("booking", {}, limit)
    return {"items": items, "count": len(items), "timestamp": datetime.utcnow()}

# Expenses
@app.post("/expenses")
def create_expense(expense: Expense):
    doc = create_document("expense", expense)
    return doc

@app.get("/expenses", response_model=ListResponse)
async def list_expenses(limit: Optional[int] = 100):
    items = get_documents("expense", {}, limit)
    return {"items": items, "count": len(items), "timestamp": datetime.utcnow()}
