from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Format: postgresql://[user]:[password]@[host]:[port]/[database_name]
# Assuming you created a database named 'fastapi_db' in pgAdmin
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:rs9551Jy@localhost:5432/fastapi_db"

# The engine handles the connection to Postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# This creates a "Session" class. Each time we talk to the DB, we use an instance of this.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the base class that our models (like Products) will inherit from
Base = declarative_base()