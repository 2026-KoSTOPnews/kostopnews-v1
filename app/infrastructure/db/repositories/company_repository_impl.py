from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.company.company_repository import CompanyRepository
from app.apis.schemas.company import Company
from app.infrastructure.db.models.company_entity import CompanyEntity

class SqlAlchemyCompanyRepository(CompanyRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[Company]:
        """
        모든 회사 조회
        """
        companies = self.db.query(CompanyEntity).all()

        return [_to_domain(company) for company in companies]

    def find_by_id(self, company_id: int) -> Optional[Company]:
        """
        단일 회사 조회
        """
        company = (self.db.query(CompanyEntity)
                   .filter(CompanyEntity.id == company_id)
                   .first())

        return _to_domain(company) if company is not None else None

    def find_by_name(self, keyword: str) -> Optional[Company]:
        """
        키워드와 같은 회사명을 가진 단일 회사 조회
        """
        company = (self.db.query(CompanyEntity)
                   .filter(CompanyEntity.name == keyword)
                   .first())

        return _to_domain(company) if company is not None else None

    def find_all_by_name(self, keyword: str) -> List[Company]:
        """
        회사명에 입력 키워드가 포함된 모든 회사 조회
        """
        companies = (self.db.query(CompanyEntity)
                     .filter(CompanyEntity.name.ilike(f"%{keyword}%"))
                     .all())

        return [_to_domain(company) for company in companies]

def _to_domain(entity: CompanyEntity) -> Company:
    return Company(
        id=entity.id,
        name=entity.name,
        market=entity.market,
        code=entity.code,
        theme=entity.theme,
        sector=entity.sector
    )