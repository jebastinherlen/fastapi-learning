import models
import schemas
from security import (require_admin)
from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

def check_oders():
    return {"message":"working"}