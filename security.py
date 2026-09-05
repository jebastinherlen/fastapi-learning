import bcrypt
import os
import models
from sqlalchemy.orm import Session
from database import SessionLocal
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException

bearer_scheme = HTTPBearer()

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

def verify_password(plain_password:str,hashed_password:str)-> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        JWT_SECRET,
        algorithm=ALGORITHM
    )

def get_token(
        credantials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    return credantials.credentials

def get_current_user(
        credantials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: Session = Depends(get_db)
):
    token = credantials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        
        user_id = int(user_id)

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="user not found"
        )
    return user

def require_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="users/login"
)