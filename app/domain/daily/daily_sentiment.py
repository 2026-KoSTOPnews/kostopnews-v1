from dataclasses import dataclass
from datetime import date

@dataclass
class DailySentiment:
    id: int
    company_id: int
    company_name: str
    analyzed_at: date
    summary: str
    sentiment: str
    score: float