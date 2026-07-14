from sqlalchemy import Column, String, DateTime,Integer, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class APIKey(Base):
    __tablename__ = "api-key"

    api_key = Column("api-key", String(255), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    hit_count = Column(Integer, default=0)
    last_used_at = Column(
        DateTime(timezone=True),
        nullable=True
    )