from fastapi import FastAPI

# 1. Create the App instance
app = FastAPI()

# 2. Define a "Home" route
@app.get("/")
def home():
    return {
        "message": "Hala Madrid!", 
        "status": "Server is live",
        "version": "0.135.x"
    }

# 3. Define a "Predictor" route (for your DSA skills)
@app.get("/sum-check")
def check_sum(a: int, b: int):
    return {"result": a + b}