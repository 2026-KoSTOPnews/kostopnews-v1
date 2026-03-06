from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict

class NewsCollector(ABC):

    @abstractmethod
    def collect(
        self,
        keyword: str,
        start_time: datetime,
        end_time: datetime,
        max_articles: int = 50
    ) -> List[Dict]:
        """
        return:
        [
          {
            "title": str,
            "content": str,
            "published_at": datetime,
            "url": str,
            "source": str
          }
        ]
        """
        pass
