# import requests

# url = 'https://google.com'
# timeout = 1  # Timeout in seconds

# try:
#     response = requests.get(url, timeout=timeout)
#     response.raise_for_status()  # Raise an exception for HTTP errors
#     print(response.text)
# except requests.RequestException as e:
#     print(f"Error: {e}")

import supabase
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional

SUPABASE_URL = "https://pefstsckwxhvbcalqlxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBlZnN0c2Nrd3hodmJjYWxxbHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDM3NDY1ODcsImV4cCI6MjAxOTMyMjU4N30.cVr_AvYBFkfc6cLBokoYuba-RLWNLWpZ4Mdsr9Dgncs"

supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    email:str
    password:str

@app.post('/register')
async def register(user: User):
    user_data = {"email": user.email, "password": user.password}
    result = supabase_client.auth.sign_up(user_data)

    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: User):
    user_data = {"email": user.email, "password": user.password}
    
    try:
        result = supabase_client.auth.sign_in_with_password(user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if hasattr(result, 'error') and result.error:
        # Access the message property of the error object
        error_message = result.error.message
        raise HTTPException(status_code=400, detail=error_message)

    return {"message": "User logged in successfully", "access_token": "access_tokens"}