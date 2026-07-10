from sqlalchemy.orm import Session
from models import History,User
from auth import hash_password

def save_cal(db:Session,expression:str,result:float):
    h=History(expression=expression,result=result)
    db.add(h)
    db.commit()
    # this updates the py object with the latest data or values from the database or mysql.
    db.refresh(h)
    return h

def get_history(db:Session):
    return db.query(History).all()

def delete_history(db:Session,id:int):
    h=db.query(History).filter(History.id==id).first()

    if h is None:
        return None
    db.delete(h)
    db.commit()

    return h
def create_user(db:Session,name:str,email:str,password:str):
    hashed_pass=hash_password(password)
    new_user=User(name=name,email=email,password=hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def verify_user(db:Session, email:str):
    # normalize for safer matching (prevents whitespace/case issues)
    if email is None:
        return None
    normalized_email = email.strip()
    user = db.query(User).filter(User.email == normalized_email).first()
    return user

   