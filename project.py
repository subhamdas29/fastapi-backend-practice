from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from models import ProductSchema
# 1. This command tells Postgres to create the table if it doesn't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
products=[
    ProductSchema(id=3,type="hello"),ProductSchema(id=4,type="bye"),ProductSchema(id=5,type="yes"),ProductSchema(id=6,type="no")
]
# 2. Dependency: This ensures the DB connection is closed after every request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def init_db():
    db=SessionLocal()
    for productt in products:
        db.add(models.ProductDB(**productt.model_dump())) # 1 & 2 below the full code
    db.commit()


def checkF():
    db = SessionLocal()
    # Check if we already have products
    count = db.query(models.ProductDB).count()
    if count <3:
        init_db()
    db.close()

checkF()



@app.get("/")
def home():
    return {"message": "Server is running!"}

# 3. GET ALL - Reads from the 'inventory' table
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.ProductDB).all()
    return products

# 4. GET ONE - Search by ID in Postgres
@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(models.ProductDB).filter(models.ProductDB.id == id).first()
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")

# 5. POST - Save a new product to Postgres
@app.post("/products")
def add_product(product_data: models.ProductSchema, db: Session = Depends(get_db)):
    new_product = models.ProductDB(id=product_data.id, type=product_data.type)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# 6. PUT - Update an existing record
@app.put("/products/{id}")
def update_product(id: int, product_data: models.ProductSchema, db: Session = Depends(get_db)):
    db_product = db.query(models.ProductDB).filter(models.ProductDB.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.type = product_data.type
    db.commit()
    return {"message": "Product updated successfully"}

# 7. DELETE - Remove a record from Postgres
@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.ProductDB).filter(models.ProductDB.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}


# 1. productt.model_dump() (The Translator)
# Before this line, your data is inside a Pydantic model (the ProductSchema). Think of this like a specialized container that is great for checking errors but the database doesn't understand it.
# What happens: .model_dump() takes that container and "dumps" the data into a standard Python Dictionary.
# The Result: It turns your object into this: {"id": 1, "type": "abc"}


# 2. #The ** (The Unpacker)
# This is called the "Spread" or "Unpacking" operator. It’s a shortcut so you don't have to type everything manually.
# Without **: You would have to write:
# models.ProductDB(id=dictionary["id"], type=dictionary["type"])
# With **: It automatically takes the Keys (id, type) and Values (1, "abc") from the dictionary and lays them out perfectly for the next step.
# The Result: It prepares the command to look like this: ProductDB(id=1, type="abc")