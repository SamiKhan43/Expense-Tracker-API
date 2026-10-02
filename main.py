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
    
# This functions ONLY job is to:
#   1. Open a fresh connection "session" to the database
#   2. Hand that connection over to whichever endpoint needs it
#   3. ALWAYS close the connection afterward, even if something crashes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def welcome_massage():
    return {"message": "welcome to the Expense Tracker API"}

@app.post("/signup")

@app.post("/login")

