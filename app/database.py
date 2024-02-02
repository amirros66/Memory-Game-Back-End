import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# create a database url for sqlalchemy
DATABASE_URL = os.environ.get(
    "DATABASE_URL") or "postgresql://postgres:secret@localhost:5432/postgres"

# create SQLAlchemy engine
engine = create_engine(DATABASE_URL.replace(
    "postgres://", "postgresql://"))

# create SessionLocal class with sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class, will use later to create models or classes
Base = declarative_base()
