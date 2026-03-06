class DailySentimentNotFound(Exception):
    def __init__(self, daily_id: int):
        super().__init__(f"Daily Sentiment not found: {daily_id}")
        self.daily_id = daily_id