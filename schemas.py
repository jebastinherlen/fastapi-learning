from pydantic import BaseModel, ConfigDict, Field, EmailStr

class ProductCreate(BaseModel):
    name: str = Field(min_length=2,max_length=100)
    price: float = Field(gt=0)
    in_stock: bool = True

class UserCreate(BaseModel):
    name: str = Field(min_length=4,max_length=40)
    email: EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str = Field(min_length=8)

class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)



class ProductResponse(BaseModel):
    id: int 
    name: str
    price: float
    in_stock: bool

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr

    model_config = ConfigDict(from_attributes=True)  

class CategoriesResponse(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)