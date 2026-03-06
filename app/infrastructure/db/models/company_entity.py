from sqlalchemy import Column, BIGINT, String, Date
from app.infrastructure.db.session import Base

class CompanyEntity(Base):
    __tablename__ = "companies"

    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=False)
    market = Column(String, nullable=False) # KOSPI 또는 KOSDAQ
    code = Column(String, nullable=True)
    theme = Column(String, nullable=True)
    sector = Column(String, nullable=True)
