from fastapi import APIRouter,HTTPException,Depends
from database import SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
from pydantic import BaseModel


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

def get_products():
    return {
        "message":"Products route"
    }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/",status_code=200,response_model=list[schemas.ProductResponse])
def list_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).order_by(models.Product.id.asc()).all()
    return products

@router.post("/product", 
            status_code=201,
            response_model=schemas.ProductResponse
        )
def create_product(
    product: schemas.ProductCreate,
    db=Depends(get_db)
    ):
    db_product = models.Product(
        name=product.name,
        price=product.price,
        in_stock=product.in_stock)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/id/{product_id}",status_code=200,response_model=schemas.ProductResponse)
def get_product_by_id(product_id : int,db: Session = Depends(get_db)):
    product = (db.query(models.Product).filter(models.Product.id == product_id).first())
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )
    return product


@router.get("/stock",status_code=200)
def get_available_stocks(db : Session = Depends(get_db)):
    product = (db.query(models.Product)
               .filter(models.Product.in_stock == True)
               .filter(models.Product.price < 3000).all()
               )
    return product

@router.get("/p")
def get_products(skip: int = 0, limit: int = 10, db : Session = Depends(get_db)):
    product = db.query(models.Product).offset(skip).limit(limit).all()
    return product 

@router.get("/search")
def get_search(name: str, db: Session = Depends(get_db)):
    product = (db.query(models.Product).filter(models.Product.name == name).all())
    return product

@router.post("/categories",status_code=201,response_model=schemas.CategoriesResponse)
def create_category(category: schemas.CategoryCreate,db=Depends(get_db)):
    db_category = models.Category(name=category.name)
    

    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/{product_id}",response_model=schemas.ProductResponse)
def put_products(product_id:int, updated_product:schemas.ProductCreate, db:Session = Depends(get_db)):
    product = (db.query(models.Product).filter(models.Product.id == product_id).first())
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )
    product.name = updated_product.name
    product.price = updated_product.price
    product.in_stock = updated_product.in_stock

    db.commit()
    db.refresh(product)

    return product

@router.delete("/{product_id}")
def delete_product(product_id:int, db:Session = Depends(get_db)):
    product = (db.query(models.Product).filter(models.Product.id == product_id).first())
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {"message":"product deleted"}