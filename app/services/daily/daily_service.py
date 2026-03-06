from sqlalchemy.orm import Session

from datetime import date

from app.infrastructure.db.repositories.company_repository_impl import SqlAlchemyCompanyRepository as CompanyRepository
from app.infrastructure.db.repositories.daily_repository_impl import SqlAlchemyDailySentimentRepository as DailySentimentRepository
from app.services.daily.daily_exception import DailySentimentNotFound
from app.services.daily.daily_pipeline import DailySentimentPipeline


class DailySentimentService:

    def __init__(self, db: Session, pipeline: DailySentimentPipeline = None):
        self.db = db
        self.repository = DailySentimentRepository(db)
        self.company_repository = CompanyRepository(db)
        self.pipeline = pipeline

    def get_daily_sentiment(self, daily_id: int):
        sentiment = self.repository.find_by_id(daily_id)

        if sentiment is None:
            raise DailySentimentNotFound(daily_id)

        return sentiment

    def get_daily_sentiments_by_analyzed_at(self, analyzed_at: date):
        sentiments = self.repository.find_all_by_analyzed_at(analyzed_at)
        return sentiments

    def get_daily_sentiments_by_company_name(self, company_name: str):
        sentiments = self.repository.find_all_by_company_name(company_name)
        return sentiments

    def create_daily_sentiment(self, result):
        sentiment = self.repository.save_daily_sentiment(result)
        return sentiment

    def run_daily(self, target_date: date | None = None):
        companies = self.company_repository.find_all()

        for company in companies:
            try:
                result = self.pipeline.run_for_company(
                    company_id=company.id,
                    company_name=company.name,
                    target_date=target_date
                )

                self.create_daily_sentiment(result)

            except Exception as e:
                print(
                    f"[ERROR][DAILY] "
                    f"company={company.name} "
                    f"reason={e}"
                )
                continue