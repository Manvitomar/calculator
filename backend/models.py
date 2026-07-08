from sqlalchemy import Column,String,Integer,Float,DateTime
from datetime import datetime
from database import Base

# by inheriting the history class with the base class it tells the sqlalchemy that this class is a database table.
class History(Base):
  # It tells the sqlalchemy that creates a table named history inside mysql
   __tablename__="history"
   id=Column(Integer,primary_key=True,index=True)
   expression=Column(String(100))
   result=Column(Float)
   created_at=Column(DateTime,default=datetime.now)

  #  each object of the history class will become the row in the history table.
  # what is session:session is the temporary connection blw your python code and the database.