from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models
from ..schemas import UserCreate

router = APIRouter()


@router.post("/")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
	existing = db.query(models.User).filter(models.User.email == payload.email).first()
	if existing:
		raise HTTPException(status_code=409, detail="User already exists")
	user = models.User(email=payload.email, name=payload.name)
	db.add(user)
	db.commit()
	db.refresh(user)
	return {"id": user.id, "email": user.email, "name": user.name} 