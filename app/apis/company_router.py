from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.deps import get_db

from app.apis.schemas.company import Company
from app.services.company.company_service import CompanyService

router = APIRouter(prefix="/company")

@router.get("/all", response_model=List[Company])
def summarize_until_now(db: Session = Depends(get_db)):
    """
    전체 기업명 조회
    """
    service = CompanyService(db)
    companies = service.get_companies()
    return companies