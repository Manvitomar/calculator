from fastapi import FastAPI
from pydantic import BaseModel
from database import sessionLocal
# Import models so SQLAlchemy knows what tables to create.
from models import History  
from database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()
@app.get("/catalog")
def home():
    return {"message": "Welcome to the Calculator API!"}
@app.get("/about")
def about():
    return {"project":"calculator",
            "version":"1.0.0",
            "author":"Manvi"}


class calculation(BaseModel):
    expression: str
    result: float


@app.post('/calculate')
def calculate(data: calculation):
    db=sessionLocal()
    h=History(expression=data.expression,result=data.result)
    try:
      db.add(h)
      db.commit()
    finally:
     db.close()
    return {"message":"Done successfully"}