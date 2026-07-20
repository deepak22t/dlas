# app/api/deps.py
import uuid
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.tenant import User

def get_current_user(db: Session = Depends(get_db)) -> User:
    # Dev mode me hum directly apna seed user utha lenge
    test_user_id = uuid.UUID("22222222-2222-2222-2222-222222222222")
    user = db.query(User).filter(User.id == test_user_id).first()
    if not user:
        raise HTTPException(status_code=500, detail="Seed user not found in DB. Please run Milestone 2.1 SQL.")
    return user