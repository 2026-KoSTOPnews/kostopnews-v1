import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict

from .base import NewsCollector

class EdailyCollector(NewsCollector):
    BASE_URL = "https://www.edaily.co.kr/search/news"
    HEADERS = {"User-Agent": "Mozilla/5.0"}

    def collect(
        self,
        keyword: str,
        start_time: datetime,
        end_time: datetime,
        max_articles: int = 50
    ) -> List[Dict]:
        articles = []
        page = 1

        while len(articles) < max_articles:
            params = {
                "keyword": keyword,
                "page": page
            }

            resp = requests.get(self.BASE_URL, params=params, headers=self.HEADERS, timeout=10)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            items = soup.select("div.news_list > ul > li")
            time.sleep(1)

            if not items:
                break

            for item in items:
                link = item.select_one("a")
                date = item.select_one("span.date")

                if not link or not date:
                    continue

                url = link["href"]
                published_at = self._parse_datetime(date.text.strip())

                if published_at < start_time:
                    return articles
                if published_at > end_time:
                    continue

                article = self._fetch_article(url, published_at)
                if article:
                    articles.append(article)

                if len(articles) >= max_articles:
                    break

                time.sleep(1)

            page += 1

        return articles

    def _fetch_article(self, url, published_at):
        resp = requests.get(url, headers=self.HEADERS, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        title = soup.select_one("h1")
        content = soup.select_one("div#newsContent")

        if not title or not content:
            return None

        return {
            "title": title.text.strip(),
            "content": content.get_text(strip=True),
            "published_at": published_at,
            "url": url,
            "source": "edaily"
        }

    def _parse_datetime(self, text: str) -> datetime:
        return datetime.strptime(text, "%Y-%m-%d %H:%M")
