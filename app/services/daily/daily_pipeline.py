from concurrent.futures.thread import ThreadPoolExecutor
from datetime import date, timedelta
from typing import List

from app.apis.schemas.daily_sentiment import DailySentiment

from app.infrastructure.news.collector.base import NewsCollector
from app.infrastructure.sentiment.sentiment import SentimentAnalyzer
from app.infrastructure.summarizer.summarizer import NewsSummarizer
from app.utils.article_deduplicator import ArticleDeduplicator

class DailySentimentPipeline:
    """
    하루 단위 기업 뉴스 감정 분석 파이프라인

    흐름:
    1. 기사 수집
    2. 기사 중복 제거
    3. 하루 기사 종합 요약 (OpenAI)
    4. 요약 결과 감정 분석 (KoBERT)
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

    def run_for_company(
        self,
        company_id: int,
        company_name: str,
        target_date: date
    ) -> DailySentiment | None:
        start_time = target_date
        end_time = start_time + timedelta(days=1)

        # 1️⃣ 기사 수집 (병렬)
        all_articles = []

        def collect_from(collector):
            return collector.collect(
                keyword=company_name,
                start_time=start_time,
                end_time=end_time,
                max_articles=10
            )

        with ThreadPoolExecutor(max_workers=len(self.collectors)) as executor:
            results = executor.map(collect_from, self.collectors)

        for articles in results:
            all_articles.extend(articles)

        # 2️⃣ 중복 제거
        all_articles = self.deduplicator.deduplicate(all_articles)

        # 3️⃣ 하루 요약 (Gemini)
        summary = self.summarizer.summarize(all_articles)

        # 4️⃣ 하루 감정 분석 (KoBERT)
        sentiment, score = self.analyzer.analyze(summary)

        result = DailySentiment(
            id=0,
            company_id=company_id,
            company_name=company_name,
            analyzed_at=start_time,
            summary=summary,
            sentiment=sentiment,
            score=score
        )

        return result