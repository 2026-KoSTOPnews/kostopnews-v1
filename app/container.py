from app.infrastructure.news.factory import NewsCollectorFactory
from app.infrastructure.sentiment.kobert_loader import load_kobert_onnx
from app.infrastructure.sentiment.sentiment import SentimentAnalyzer
from app.infrastructure.summarizer.summarizer import NewsSummarizer
from app.services.daily.daily_pipeline import DailySentimentPipeline
from app.services.user.user_pipeline import UserSentimentPipeline


def create_user_pipeline():
    collectors = NewsCollectorFactory.create_all()

    session, tokenizer = load_kobert_onnx()

    return UserSentimentPipeline(
        collectors=collectors,
        summarizer=NewsSummarizer(),
        analyzer=SentimentAnalyzer(session, tokenizer),
    )

def create_daily_pipeline():
    collectors = NewsCollectorFactory.create_all()

    session, tokenizer = load_kobert_onnx()

    return DailySentimentPipeline(
        collectors=collectors,
        summarizer=NewsSummarizer(),
        analyzer=SentimentAnalyzer(session, tokenizer),
    )