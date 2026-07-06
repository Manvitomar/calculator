from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


# sqlachemy --->creates a connection blw database and python

# This is called the connection string.
DATABASE_URL = "mysql+pymysql://root:manu99@localhost:3306/calculator_db"
# it establish a connection blw the python and mysql
engine = create_engine(DATABASE_URL)
sessionLocal=sessionmaker(bind=engine)
# Think of it as a template for all database tables.
Base=declarative_base()    


