import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Booking, Expense, Client, Venue

app = FastAPI(title="VenueOS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "VenueOS Backend Running"}


@app.get("/test")
def test_database():
    """Test endpoint to verify database connectivity and show basic info"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "collections": [],
    }

    try:
        if db is not None:
            response["database"] = "✅ Connected"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, "name", None) or "✅ Set"
            try:
                response["collections"] = db.list_collection_names()[:20]
            except Exception as e:
                response["database"] = f"⚠️ Connected but error listing collections: {str(e)[:80]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


# --------- Bookings ---------
@app.post("/bookings", response_model=dict)
def create_booking(booking: Booking):
    try:
        booking_id = create_document("booking", booking)
        return {"id": booking_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/bookings", response_model=List[dict])
def list_bookings(limit: Optional[int] = 50):
    try:
        docs = get_documents("booking", {}, limit)
        # Convert ObjectId for JSON serialization
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------- Expenses ---------
@app.post("/expenses", response_model=dict)
def create_expense(expense: Expense):
    try:
        exp_id = create_document("expense", expense)
        return {"id": exp_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/expenses", response_model=List[dict])
def list_expenses(limit: Optional[int] = 100):
    try:
        docs = get_documents("expense", {}, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------- Clients ---------
@app.post("/clients", response_model=dict)
def create_client(client: Client):
    try:
        client_id = create_document("client", client)
        return {"id": client_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/clients", response_model=List[dict])
def list_clients(limit: Optional[int] = 100):
    try:
        docs = get_documents("client", {}, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------- Venues ---------
@app.post("/venues", response_model=dict)
def create_venue(venue: Venue):
    try:
        venue_id = create_document("venue", venue)
        return {"id": venue_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/venues", response_model=List[dict])
def list_venues(limit: Optional[int] = 100):
    try:
        docs = get_documents("venue", {}, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
