from pydantic import BaseModel
from datetime import date

class DailySentiment(BaseModel):
    id: int
    company_id: int
    company_name: str
    analyzed_at: date
    summary: str
    sentiment: str
    score: float

    class Config:
        from_attributes = True  # Pydantic v2용 (v1은 orm_mode=True)