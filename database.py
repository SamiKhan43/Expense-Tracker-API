from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# This cconnects to a database file called "expenses.db"
engine = create_engine("sqlite:///expenses.db")

# This is the base that all our tables will be built from
Base = declarative_base()

# This lets us open conversations with the database to save or read data
SessionLocal = sessionmaker(bind=engine)

"""
We are using SQLAlchemy instead of writing SQL queries directly because
SQLAlchemy allows us to interact with the database using Python code.
It provides an easier and more organized way to create tables, insert,
update, delete and retrieve data without having to write raw SQL for
every database operation.
"""
