from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    in_stock: bool = True

class UserCreate(BaseModel):
    name: str
    email: str

class CategoryCreate(BaseModel):
    name: str