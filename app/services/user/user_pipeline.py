from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import List

from app.apis.schemas.user_sentiment import UserSentiment

from app.infrastructure.news.collector.base import NewsCollector
from app.infrastructure.sentiment.sentiment import SentimentAnalyzer
from app.infrastructure.summarizer.summarizer import NewsSummarizer
from app.utils.article_deduplicator import ArticleDeduplicator

class UserSentimentPipeline:
    """
    사용자 요청 기반 뉴스 감정 분석 파이프라인

    흐름:
    1. 사용자 요청 시점까지 기사 수집
    2. 기사 종합 요약 (OpenAI)
    3. 요약 결과 감정 분석 (KoBERT)
    4. 사용자별 결과 DB 저장
    """

    def __init__(
        self,
        collectors: List[NewsCollector],
        summarizer: NewsSummarizer,
        analyzer: SentimentAnalyzer
    ):
        self.collectors = collectors
        self.summarizer = summarizer
        self.analyzer = analyzer
        self.deduplicator = ArticleDeduplicator()

    def run_for_user(
        self,
        user_id: str,
        company_id: int,
        company_name: str,
        request_time: datetime | None = None
    ) -> UserSentiment | None:
        if request_time is None:
            request_time = datetime.now()

        start_time = request_time.replace(
            hour = 0, minute = 0, second = 0, microsecond = 0

        )
        end_time = start_time + timedelta(days=1)

        # 1️⃣ 기사 수집
        all_articles = []

        def collect_from(collector):
            return collector.collect(
                keyword=company_name,
                start_time=start_time,
                end_time=end_time,
                max_articles=50
            )

        with ThreadPoolExecutor(max_workers=len(self.collectors)) as executor:
            results = executor.map(collect_from, self.collectors)

        for articles in results:
            all_articles.extend(articles)

        # 2️⃣ 중복 제거
        all_articles = self.deduplicator.deduplicate(all_articles)

        # 3️⃣ 사용자 요청 기준 요약
        summary = self.summarizer.summarize(all_articles)

        # 4️⃣ 감정 분석 (KoBERT)
        sentiment, score = self.analyzer.analyze(summary)

        result = UserSentiment(
            id=0,
            company_id=company_id,
            company_name=company_name,
            created_at=request_time.date(),
            summary=summary,
            sentiment=sentiment,
            score=score,
            user_id=str(user_id),
            article_count=len(all_articles)
        )

        return result
