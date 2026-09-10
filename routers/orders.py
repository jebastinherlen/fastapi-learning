import models
import schemas
from security import (get_current_user)
from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{order_id}",status_code=200,)
def check_oders(order_id: int, db:Session= Depends(get_db), current_user: models.User = Depends(get_current_user)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    if order.user_id != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="you cannot access this order"
        )

    
    return order
