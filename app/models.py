from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class AuthProvider(enum.Enum):
    LOCAL = "local"
    GOOGLE = "google"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255))
    hashed_password = Column(String(255), nullable=True)
    google_id = Column(String(255), unique=True, index=True, nullable=True)
    auth_provider = Column(String(50), default="local")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
