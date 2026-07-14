from fastapi import Header, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.database import SessionLocal
from app.models import APIKey


MAX_REQUESTS = 1000
TIME_WINDOW = 60   


def validate_api_key(x_api_key: str = Header(...)):

    db: Session = SessionLocal()

    try:

        key = db.query(APIKey).filter(
            APIKey.api_key == x_api_key
        ).first()


        if not key:
            raise HTTPException(
                status_code=401,
                detail="Invalid API Key"
            )


        now = datetime.now(timezone.utc)


        
        if key.last_used_at is None:

            key.last_used_at = now
            key.hit_count = 1


        else:

            time_difference = (
                now - key.last_used_at
            ).total_seconds()


            
            if time_difference >= TIME_WINDOW:

                key.last_used_at = now
                key.hit_count = 1


            
            else:
                print(f"Current hit count: {key.hit_count}")
                print(f"Time difference: {time_difference} seconds")
                print(f"Time window: {TIME_WINDOW} seconds")
                print(f"Max requests: {MAX_REQUESTS}")
                if key.hit_count >= MAX_REQUESTS:

                    raise HTTPException(
                        status_code=429,
                        detail="API rate limit exceeded. Please try again later."
                    )


                key.hit_count += 1


        db.commit()
        db.refresh(key)


        return key


    finally:
        db.close()