from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib

app = FastAPI()

# Mock database
users_db = {}

# Models for Signup and Login
class User(BaseModel):
    username: str
    password: str

# Hashing function
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/signup")
def signup(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    users_db[user.username] = hash_password(user.password)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: User):
    hashed_password = users_db.get(user.username)
    if not hashed_password or hashed_password != hash_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful"}
