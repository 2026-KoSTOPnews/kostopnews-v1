from sqlalchemy import Column, BIGINT, String, DateTime, Float, Integer, func
from app.infrastructure.db.session import Base

class UserSentimentEntity(Base):
    __tablename__ = "user_sentiments"

    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    company_id = Column(BIGINT, nullable=False)
    company_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    summary = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    user_id = Column(String, nullable=False)
    article_count = Column(Integer, nullable=False)
