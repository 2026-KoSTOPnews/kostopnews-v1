from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.deps import get_db
from datetime import date

from app.apis.schemas.daily_sentiment import DailySentiment
from app.services.daily.daily_service import DailySentimentService

router = APIRouter(prefix="/sentiment", tags=["Daily Sentiment"])

@router.get("/record/id/{daily_id}", response_model=DailySentiment)
def get_daily_record(daily_id: int, db: Session = Depends(get_db)):
    """
    해당 id의 하루치 요약 + 감정 분석 결과 조회
    """
    service = DailySentimentService(db)
    entity = service.get_daily_sentiment(daily_id)
    return entity

@router.get("/record/date/{target_date}", response_model=List[DailySentiment])
def get_daily_record_by_analyzed_at(target_date: date, db: Session = Depends(get_db)):
    """
    해당 날짜의 하루치 요약 + 감정 분석 결과 조회 (같은 날짜, 다른 기업들의 결과 조회)
    """
    service = DailySentimentService(db)
    entities = service.get_daily_sentiments_by_analyzed_at(target_date)
    return entities

@router.get("/record/{keyword}", response_model=List[DailySentiment])
def get_daily_record_by_company_name(keyword: str, db: Session = Depends(get_db)):
    """
    해당 기업의 하루치 요약 + 감정 분석 결과 조회 (같은 기업, 여러 날짜의 결과 조회)
    """
    service = DailySentimentService(db)
    entities = service.get_daily_sentiments_by_company_name(keyword)
    return entities
