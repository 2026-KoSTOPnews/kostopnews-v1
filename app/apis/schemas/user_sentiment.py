from pydantic import BaseModel
from datetime import date

class UserSentiment(BaseModel):
    id: int
    company_id: int
    company_name: str
    created_at: date
    summary: str
    sentiment: str
    score: float
    user_id: str
    article_count: int

    class Config:
        from_attributes = True  # Pydantic v2용 (v1은 orm_mode=True)
