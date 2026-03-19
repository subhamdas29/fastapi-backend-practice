from fastapi import FastAPI

app = FastAPI()
# @app.get("/")
# def home():
#     return {"message": "Server is running!"}
# 3 Segments (Most Specific)
@app.get("/{id}/{se}/add")
def operation(id: int, se: int):
    return {"data": id + se}

# 2 Segments
@app.get("/{id}/{se}")
def second(id: int, se: int): # Added 'id' here to prevent errors
    return {"data": f"Your second number is {se}"}

# 1 Segment (Most General)
@app.get("/{id}")
def first(id: int):
    return {"data": f"Your first number is {id}"}