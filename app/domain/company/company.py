from dataclasses import dataclass
from app.domain.company.market_type import MarketType

@dataclass
class Company:
    id: int
    name: str
    market: MarketType # KOSPI 또는 KOSDAQ
    code: str
    theme: str
    sector: str
