from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

# This creates the table in PostgreSQL
class ProductDB(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)

# This is still used for FastAPI validation (Pydantic)
class ProductSchema(BaseModel):
    id: int
    type: str

    class Config:
        from_attributes = True