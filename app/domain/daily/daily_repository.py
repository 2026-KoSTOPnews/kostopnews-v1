from datetime import date

from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.daily.daily_sentiment import DailySentiment

class DailySentimentRepository(ABC):

    @abstractmethod
    def find_by_id(self, daily_id: int) -> Optional[DailySentiment]:
        pass

    @abstractmethod
    def find_all_by_analyzed_at(self, target_date: date) -> List[DailySentiment]:
        pass

    @abstractmethod
    def find_all_by_company_name(self, company_name: str) -> List[DailySentiment]:
        pass

    @abstractmethod
    def save_daily_sentiment(self, result) -> DailySentiment:
        pass