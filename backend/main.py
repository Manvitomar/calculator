from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
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
    operation:str

@app.post('/calculate')
def calculate(data: calculation):
    print(data.expression)
    print(data.result)
    print(data.operation)
    return {"expression": data.expression, 
            "result": data.result,
            "operation":data.operation,
            "status":"success"}