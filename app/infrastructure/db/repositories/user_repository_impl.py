from sqlalchemy.orm import Session
from typing import List
from app.domain.user.user_repository import UserSentimentRepository
from app.apis.schemas.user_sentiment import UserSentiment
from app.infrastructure.db.models.user_entity import UserSentimentEntity

class SqlAlchemyUserSentimentRepository(UserSentimentRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_all_by_user_id(self, user_id: str) -> List[UserSentiment]:
        """
        유저 아이디 별 모든 기사 분석 조회
        """
        user_sentiments = (self.db.query(UserSentimentEntity)
                           .filter(UserSentimentEntity.user_id == user_id)
                           .all())

        return [_to_domain(us) for us in user_sentiments]

    def find_all_by_keyword_and_user_id(self, keyword: str, user_id: str) -> List[UserSentiment]:
        """
        유저 아이디 별 회사명에 입력 키워드가 포함된 모든 기사 분석 조회
        """
        user_sentiments = (self.db.query(UserSentimentEntity)
                           .filter(UserSentimentEntity.user_id == user_id)
                           .filter(UserSentimentEntity.company_name == keyword)
                           .all())

        return [_to_domain(us) for us in user_sentiments]

    def save_user_sentiment(self, result) -> UserSentiment:
        """
        기사 분석 결과 저장
        """
        entity = _to_entity(result)

        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)

        return _to_domain(entity)

    # def delete_older_than(self, user_id: str, created_at: datetime) -> int:
    #     stmt = (self.db.delete(UserSentimentEntity)
    #             .where(UserSentimentEntity.user_id == user_id,
    #                    UserSentimentEntity.created_at < created_at))
    #     result = self.db.execute(stmt)
    #     return result.rowcount

def _to_domain(entity) -> UserSentiment:
    return UserSentiment(
        id=entity.id,
        company_id=entity.company_id,
        company_name=entity.company_name,
        created_at=entity.created_at,
        summary=entity.summary,
        sentiment=entity.sentiment,
        score=entity.score,
        user_id=entity.user_id,
        article_count=entity.article_count
    )

def _to_entity(result) -> UserSentimentEntity:
    return UserSentimentEntity(
        company_id=result.company_id,
        company_name=result.company_name,
        created_at=result.created_at,
        summary=result.summary,
        sentiment=result.sentiment,
        score=result.score,
        user_id=result.user_id,
        article_count=result.article_count
    )