import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

_client: Optional[MongoClient] = None
_db = None

def get_db():
    global _client, _db
    if _db is not None:
        return _db
    _client = MongoClient(DATABASE_URL, server_api=ServerApi("1"))
    _db = _client[DATABASE_NAME]
    return _db

# Helper utilities

def _to_dict(model: Any) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    if hasattr(model, "dict"):
        return model.dict()
    return dict(model)


def create_document(collection_name: str, data: Any) -> Dict[str, Any]:
    db = get_db()
    payload = _to_dict(data)
    now = datetime.utcnow()
    payload["created_at"] = now
    payload["updated_at"] = now
    res = db[collection_name].insert_one(payload)
    payload["_id"] = str(res.inserted_id)
    return payload


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
    db = get_db()
    filt = filter_dict or {}
    docs = list(db[collection_name].find(filt).limit(limit))
    # Convert ObjectId to str
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs
