from typing import Dict, Type, List

from app.infrastructure.news.collector.base import NewsCollector
from app.infrastructure.news.collector.yeonhap import YeonhapCollector
from app.infrastructure.news.collector.mk import MkCollector
from app.infrastructure.news.collector.hankyung import HankyungCollector
from app.infrastructure.news.collector.sedaily import SedailyCollector
from app.infrastructure.news.collector.edaily import EdailyCollector

class NewsCollectorFactory:
    _collectors: Dict[str, Type[NewsCollector]] = {
        "yeonhap": YeonhapCollector,
        "mk": MkCollector,
        # "hankyung": HankyungCollector,
        # "sedaily": SedailyCollector,
        # "edaily": EdailyCollector,
    }

    @classmethod
    def create(cls, source: str) -> NewsCollector:
        source = source.lower()

        if source not in cls._collectors:
            raise ValueError(f"Unsupported news source: {source}")

        return cls._collectors[source]()

    @classmethod
    def create_all(cls) -> List[NewsCollector]:
        return [collector() for collector in cls._collectors.values()]

    @classmethod
    def supported_sources(cls) -> List[str]:
        return list(cls._collectors.keys())
