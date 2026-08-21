from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message":"Hello FastAPI"}

@app.get("/about")
def home():
    return {"message":"About API"}

@app.get("/user")
def get_user():
    return {
        "name":"herlen",
        "age":24,
        "developer": True
    }

@app.get("/products")
async def get_product():
    return {
        "products": []
    }

