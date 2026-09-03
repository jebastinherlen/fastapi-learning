from sqlalchemy import Column, Integer, String, Float,  Boolean

from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    in_stock = Column(Boolean)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)