from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)

    email = Column(String(300))
    phone = Column(Integer)
    
    def __init__(self, firstname: str, lastname: str, phone: int):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone


    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'