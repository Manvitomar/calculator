from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from crud import save_cal, get_history, delete_history
from database import sessionLocal
# Import models so SQLAlchemy knows what tables to create.
from models import History
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Create tables on startup (will NOT alter existing tables)
Base.metadata.create_all(bind=engine)
app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent.parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "frontend"),
    name="static"
)
app.add_middleware(
    CORSMiddleware,
   allow_origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://calculator-eta-bice.vercel.app"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return FileResponse(BASE_DIR / "frontend" / "index.html")
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
    try:
      h=save_cal(db=db,expression=data.expression,result=data.result)
      return {"message":"Done successfully","id":h.id}

    finally:
     db.close()

@app.get('/history')
def history():
        # create a session object to connect to the database and perform operations. ...or... 
        # a session is used to commuicate with the database.now the gate is open to communicate with the database and perform operations like insert, update, delete, and query.
        db=sessionLocal()
        try:
         data=get_history(db=db)
         return data
        finally:
         db.close()    

@app.delete('/history/{id}')
def remove_history(id:int):
    db=sessionLocal()
    try:
       deleted=delete_history(db,id)
       if deleted:
           return {"message":"Record deleted successfully"}
       else:
           return {"message":"Record not found"}
    finally:
        db.close()