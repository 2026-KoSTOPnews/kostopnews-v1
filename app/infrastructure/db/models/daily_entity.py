from sqlalchemy import Column, BIGINT, String, Date, Float, func
from app.infrastructure.db.session import Base

class DailySentimentEntity(Base):
    __tablename__ = "daily_sentiments"

    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    company_id = Column(BIGINT, nullable=False)
    company_name = Column(String, nullable=False)
    analyzed_at = Column(Date, nullable=False, server_default=func.current_date())
    summary = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)
    score = Column(Float, nullable=False)
