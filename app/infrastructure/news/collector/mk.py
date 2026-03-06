import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict

from .base import NewsCollector

class MkCollector(NewsCollector):
    BASE_URL = "https://www.mk.co.kr/search"
    HEADERS = {
        "User-Agent": "Mozilla/5.0"
    }

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
                "word": keyword,
                "page": page
            }

            resp = requests.get(self.BASE_URL, params=params, headers=self.HEADERS, timeout=10)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            items = soup.select("div.search_list > ul > li")
            time.sleep(1)

            if not items:
                break

            for item in items:
                link_tag = item.select_one("a")
                date_tag = item.select_one("span.date")

                if not link_tag or not date_tag:
                    continue

                url = link_tag["href"]
                published_at = self._parse_datetime(date_tag.text.strip())

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

    def _fetch_article(self, url: str, published_at: datetime) -> Dict | None:
        resp = requests.get(url, headers=self.HEADERS, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.select_one("h2.tit")
        content_tag = soup.select_one("div#article_body")

        if not title_tag or not content_tag:
            return None

        return {
            "title": title_tag.text.strip(),
            "content": content_tag.get_text(strip=True),
            "published_at": published_at,
            "url": url,
            "source": "mk"
        }

    def _parse_datetime(self, text: str) -> datetime:
        # 예: 2026.01.27 14:32
        return datetime.strptime(text, "%Y.%m.%d %H:%M")
