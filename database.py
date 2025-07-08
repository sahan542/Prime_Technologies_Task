from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

# Replace with your actual PostgreSQL connection string
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://doadmin:AVNS_a8ujVV5Kz17xSRI0Ha1@db-postgresql-blr1-61912-do-user-23749570-0.m.db.ondigitalocean.com:25060/defaultdb?sslmode=require")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
