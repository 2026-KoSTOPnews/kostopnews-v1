from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserSentiment:
    id: int
    company_id: int
    company_name: str
    created_at: datetime
    summary: str
    sentiment: str
    score: float
    user_id: str # UUID
    article_count: int
