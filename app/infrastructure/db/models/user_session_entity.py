from sqlalchemy import Column, String, DateTime, func
from app.infrastructure.db.session import Base

class UserSessionEntity(Base):
    __tablename__ = "user_sessions"

    user_id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_seen_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())