from pydantic import BaseModel,EmailStr
# schema file mai basically hum incoming data ka formate check krtai hai shi hai ya nahi
class UserCreate(BaseModel):
  name:str
  email:EmailStr
  password:str

class UserLogin(BaseModel):
  email:EmailStr
  password:str

  