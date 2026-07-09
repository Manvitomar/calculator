from sqlalchemy.orm import Session
from models import History

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