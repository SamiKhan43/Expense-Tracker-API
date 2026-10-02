from fastapi import FastAPI, Depends
from pydantic import BaseModel
from pwdlib import PasswordHash
from database import Base, engine, SessionLocal

app = FastAPI()
Base.metadata.create_all(bind=engine)
password_hash = PasswordHash.recommended()

# This describes what data we expect someone to send us when signing up.
class UserCreate(BaseModel):
    username: str
    password: str
  
# This describes what data we expect someone to send us when he login.
class UserLogin(BaseModel):
    username : str
    password : str

@app.get("/")
def welcome_massage():
    return {"message": "welcome to the Expense Tracker API"}
