from fastapi import APIRouter,HTTPException,Depends
from database import SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
from security import (hash_password, verify_password, create_access_token, get_current_user, require_admin)


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

@router.get("/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.post("/register",status_code=201,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate,db=Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=("Email already registered")
        )

    hashed_password = hash_password(user.password)
    
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/",status_code=200,response_model=list[schemas.UserResponse])
def get_user(db: Session = Depends(get_db)):
    user = (db.query(models.User).order_by(models.User.id.asc()).all())
    return user

@router.put("/edit/{user_id}",status_code=200,response_model=schemas.UserResponse)
def update_user(user_id: int,update_user:schemas.UserCreate,db: Session = Depends(get_db)):
    user = (db.query(models.User).filter(models.User.id == user_id).first())
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    hashed_password = hash_password(update_user.password)

    user.name = update_user.name
    user.email = update_user.email
    user.hashed_password = hashed_password

    db.commit()
    db.refresh(user)

    return user

@router.post("/login",status_code=200)
def user_login(user:schemas.UserLogin, db:Session = Depends(get_db)):
    existing_user = (db.query(models.User).filter(models.User.email == user.email).first())
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        existing_user.hashed_password
    ):
        
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": str(existing_user.id)
        }
    )
    
    return {
        "access_token": access_token,
        "token_type":"bearer",
        "message":"Login successfull"
        }