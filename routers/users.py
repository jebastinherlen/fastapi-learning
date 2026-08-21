from fastapi import APIRouter,HTTPException,Depends
from database import SessionLocal
from sqlalchemy.orm import Session
import models
import schemas


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_users():
    return {"message":"Users route"}

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

@router.post("/register",status_code=201)
def create_user(user: schemas.UserCreate,db=Depends(get_db)):
    db_user = models.User(name=user.name,email=user.email)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/")
def get_user(db: Session = Depends(get_db)):
    user = (db.query(models.User).all())
    return user
