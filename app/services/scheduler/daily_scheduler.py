from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, timedelta
import logging

from app.infrastructure.db.session import SessionLocal
from app.services.daily.daily_service import DailySentimentService

logger = logging.getLogger(__name__)

class DailySentimentScheduler:

    def __init__(self, pipeline):
        self.scheduler = BackgroundScheduler(timezone="Asia/Seoul")
        self.pipeline = pipeline

    def start(self):
        self.scheduler.add_job(
            self.run_daily_job,
            trigger="cron",
            hour=1, # 매일 새벽 1시
            minute=0
        )
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown(wait=False)

    def run_daily_job(self):
        db = SessionLocal()

        try:
            service = DailySentimentService(db, self.pipeline)
            target_date = date.today() - timedelta(days=1)
            service.run_daily(target_date)
        except Exception as e:
            logger.exception("[Daily sentiment job failed]" + str(e))
        finally:
            db.close()