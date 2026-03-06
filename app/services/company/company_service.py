from sqlalchemy.orm import Session
from app.infrastructure.db.repositories.company_repository_impl import SqlAlchemyCompanyRepository as CompanyRepository
from app.services.company.company_exception import CompanyNotFound

class CompanyService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = CompanyRepository(db)

    def get_companies(self):
        companies = self.repository.find_all()
        return companies

    def get_company(self, company_id: int):
        company = self.repository.find_by_id(company_id)

        if company:
            raise CompanyNotFound(company_id)

        return company

    def get_companies_by_name(self, keyword: str):
        companies = self.repository.find_all_by_name(keyword)
        return companies