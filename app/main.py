# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Hello, FastAPI!"}


# @app.get("/generate-key")
# def generate_key():
#     import secrets
#     key = secrets.token_hex(16)
#     return {"key": key}


from fastapi import FastAPI
from sqlalchemy.orm import Session
import secrets

from app.database import SessionLocal
from app.models import APIKey
from fastapi import FastAPI, Depends
from app.dependencies import validate_api_key

app = FastAPI()


@app.post("/generate-key")
def generate_key(): 

    db: Session = SessionLocal()

    try:
        key = secrets.token_hex(32)

        api_key = APIKey(api_key=key)

        db.add(api_key)
        db.commit()

        return {
            "success": True,
            "api_key": key
        }

    finally:
        db.close()


@app.get("/key-validation")
def call_external_api(
    api_key = Depends(validate_api_key)
):
    return {
        "message": "API call successful",
        "used_count": api_key.hit_count
    }