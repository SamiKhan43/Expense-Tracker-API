from fastapi import FastAPI, Depends
from pydantic import BaseModel
from pwdlib import PasswordHash
from database import Base, engine, SessionLocal
from models import User, Expense
from auth import password_hash, create_access_token, get_current_user
from fastapi import HTTPException
from datetime import date,timedelta
from typing import Optional


# Create the tables when the app starts
app = FastAPI()
Base.metadata.create_all(bind=engine)
password_hash = PasswordHash.recommended()

# Data required when creating a new account
class UserCreate(BaseModel):
    username: str
    password: str

# Data required for login
class UserLogin(BaseModel):
    username : str
    password : str

# Data required when creating/updating an expense
class ExpenseCreate(BaseModel):
    title : str
    amount : float
    category : str
    date : date
    user_id : int


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
def signup(user: UserCreate, db=Depends(get_db)):
    hashed = password_hash.hash(user.password)

    new_user = User(
        username=user.username,
        hashed_password=hashed
        )

    db.add(new_user)
    db.commit()
    
    return {"message": f"User '{user.username}' created successfully"}

@app.post("/login")
def login(user:UserLogin,db=Depends(get_db)):
        
    # Find the user by username
    db_user = db.query(User).filter(
        User.username == user.username
        ).first()

    if not db_user:
        raise HTTPException( 
            status_code=401,
            detail="invalid username or password"
    )

    if not password_hash.verify(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
        status_code=401,
        detail="invalid username or password"    
    )

    token = create_access_token(db_user.username)

    return {"access_token":token,"token_type":"bearer"}

@app.get("/profile")
def read_profile(current_user : str = Depends(get_current_user)):
    # get_current_user gets the username from the JWT
    return{"username":current_user}


@app.post("/expenses")
def add_expense(
    expense: ExpenseCreate,
    db=Depends(get_db),
    current_user: str = Depends(get_current_user)     # Get the logged in user's database record
    ):

    # Use the logged-in user's ID instead of trusting user_id from the request
    db_user = db.query(User).filter(User.username == current_user).first()
    new_expense = Expense (
        title = expense.title,
        amount = expense.amount,
        category = expense.category,
        date = expense.date,
        user_id = db_user.id
    )

    db.add(new_expense)
    db.commit()
    return{"massege":f" Expense'{expense.title}' added successfully"}

@app.get("/expenses")
def get_expenses(
    filter : Optional[str] = None, 
    start_date : Optional[date] = None,
    end_date : Optional[date] = None,
    db = Depends(get_db),
    current_user : str = Depends(get_current_user)
):
    db_user = db.query(User).filter(User.username == current_user).first()
    query = db.query(Expense).filter(Expense.user_id == db_user.id)

    today = date.today()

    if filter == "week":
        query = query.filter(
            Expense.date >= today - timedelta(days=7))

    elif filter == "month":
        query = query.filter(
            Expense.date >= today - timedelta(days=30))

    elif filter == "3months":
        query = query.filter(
            Expense.date >= today - timedelta(days=90))

    elif filter == "custom":
        if start_date:
            query = query.filter(Expense.date >= start_date)

        if end_date:
            query = query.filter(Expense.date <= end_date)

    return query.all()
            

@app.get("/expenses/{expense_id}")
def get_expense(expense_id:int , db=Depends(get_db), current_user: str = Depends(get_current_user)):
    db_user = db.query(User).filter(User.username == current_user).first()
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == db_user.id
        ).first()
    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    return expense

@app.put("/expenses/{expense_id}")
def update_expense(expense_id:int, updated:ExpenseCreate , db = Depends(get_db) , current_user : str = Depends(get_current_user)):
    db_user = db.query(User).filter(User.username == current_user).first()
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == db_user_id
        ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    expense.title = updated.title
    expense.amount = updated.amount
    expense.category = updated.category
    expense.date = updated.date

    db.commit()
    return {"message": f"Expense {expense_id} updated successfully"}

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id:int, db = Depends(get_db) , current_user : str = Depends(get_current_user)):

    db_user = db.query(User).filter(User.username == current_user).first()
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == db_user.id
        ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()
    return{"massege":f"Expense {expense_id} deleted successfully"}




