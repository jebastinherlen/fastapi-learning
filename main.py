from fastapi import FastAPI
from routers import products, users
from database import engine
from sqlalchemy import text
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)

@app.get("/db-checks")
def db_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {
            "database":"connected",
            "result":result.scalar()
        }