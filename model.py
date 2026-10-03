from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class User(Base):  # This defines a table design called "User in db"
    __tablename__ = "users"  

    id = Column(Integer, primary_key=True)  
    username = Column(String, unique=True) 
    hashed_password = Column(String)  

class Expense(Base): # This defines a table design called "Expenses in db"
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    title = Column(String)       
    amount = Column(Float)       
    category = Column(String)    
    date = Column(Date)
    user_id = Column(Integer)        


