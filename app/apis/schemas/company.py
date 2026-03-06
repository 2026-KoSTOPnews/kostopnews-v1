from pydantic import BaseModel

class Company(BaseModel):
    id: int
    name: str
    market: str  # KOSPI 또는 KOSDAQ
    code: str
    theme: str
    sector: str

    class Config:
        from_attributes = True