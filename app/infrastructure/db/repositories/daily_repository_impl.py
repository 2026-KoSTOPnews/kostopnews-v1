from datetime import date

from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.daily.daily_repository import DailySentimentRepository
from app.apis.schemas.daily_sentiment import DailySentiment
from app.infrastructure.db.models.daily_entity import DailySentimentEntity

class SqlAlchemyDailySentimentRepository(DailySentimentRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, daily_id: int) -> Optional[DailySentiment]:
        """
        해당 id의 단일 기사 분석 결과 조회
        """
        daily_sentiment = (self.db.query(DailySentimentEntity)
                           .filter(DailySentimentEntity.id == daily_id)
                           .first())

        return _to_domain(daily_sentiment) if daily_sentiment is not None else None


    def find_all_by_analyzed_at(self, target_date: date) -> List[DailySentiment]:
        """
        해당 닐짜의 기사 분석 결과 조회
        """
        daily_sentiments = (self.db.query(DailySentimentEntity)
                            .filter(DailySentimentEntity.analyzed_at == target_date)
                            .all())

        return [_to_domain(ds) for ds in daily_sentiments]

    def find_all_by_company_name(self, company_name: str) -> List[DailySentiment]:
        """
        기업명 별 기사 분석 결과 조회
        """
        daily_sentiments = (self.db.query(DailySentimentEntity)
                           .filter(DailySentimentEntity.company_name == company_name)
                           .all())

        return [_to_domain(ds) for ds in daily_sentiments]

    def save_daily_sentiment(self, result) -> DailySentiment:
        """
        기사 분석 결과 저장
        """
        entity = _to_entity(result)

        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)

        return _to_domain(entity)

def _to_domain(entity) -> DailySentiment:
    return DailySentiment(
        id=entity.id,
        company_id=entity.company_id,
        company_name=entity.company_name,
        analyzed_at=entity.analyzed_at,
        summary=entity.summary,
        sentiment=entity.sentiment,
        score=entity.score
    )

def _to_entity(result) -> DailySentimentEntity:
    return DailySentimentEntity(
        company_id=result.company_id,
        company_name=result.company_name,
        analyzed_at=result.analyzed_at,
        summary=result.summary,
        sentiment=result.sentiment,
        score=result.score
    )