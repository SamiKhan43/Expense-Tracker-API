from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):  # This defines a table design called "User"
    __tablename__ = "users"  

    id = Column(Integer, primary_key=True)  
    username = Column(String, unique=True) 
    hashed_password = Column(String)  