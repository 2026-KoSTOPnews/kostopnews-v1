from typing import List
from uuid import UUID

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from app.infrastructure.auth.deps import get_current_user_id
from app.infrastructure.db.deps import get_db
from datetime import datetime

from app.apis.schemas.user_sentiment import UserSentiment
from app.services.user.user_service import UserSentimentService

router = APIRouter(prefix="/sentiment", tags=["User Sentiment"])

@router.get("/summary/{keyword}/{until}", response_model=UserSentiment)
def summarize_until_now(keyword: str, until: datetime, request: Request, user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """
    오늘 00:00 ~ until 까지 뉴스 요약 + 감정 분석
    """
    user_id = str(user_id)
    pipeline = request.app.state.user_pipeline
    service = UserSentimentService(db, pipeline)
    entity = service.run_user(user_id=user_id, company_name=keyword, request_time=until)
    return entity

@router.get("/record", response_model=List[UserSentiment])
def get_record(user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """get_user_sentiments_by_user_id
    뉴스 요약 + 감정 분석 기록 조회
    """
    user_id = str(user_id)
    service = UserSentimentService(db)
    entities = service.get_user_sentiments_by_user_id(user_id=user_id)
    return entities

@router.get("/record/{keyword}", response_model=List[UserSentiment])
def get_record_by_keyword(keyword: str, user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """
    키워드별 뉴스 요약 + 감정 분석 기록 조회
    """
    user_id = str(user_id)
    service = UserSentimentService(db)
    entities = service.get_user_sentiments_by_keyword_and_user_id(keyword=keyword, user_id=user_id)
    return entities