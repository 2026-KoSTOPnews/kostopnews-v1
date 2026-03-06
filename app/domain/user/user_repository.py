from abc import ABC, abstractmethod
from typing import List
from app.domain.user.user_sentiment import UserSentiment

class UserSentimentRepository(ABC):

    @abstractmethod
    def find_all_by_user_id(self, user_id: str) -> List[UserSentiment]:
        pass

    @abstractmethod
    def find_all_by_keyword_and_user_id(self, keyword: str, user_id: str) -> List[UserSentiment]:
        pass

    @abstractmethod
    def save_user_sentiment(self, result) -> UserSentiment:
        pass