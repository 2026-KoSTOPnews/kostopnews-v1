import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict

from .base import NewsCollector

class HankyungCollector(NewsCollector):
    BASE_URL = "https://search.hankyung.com/apps.frm/search.news"
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
                "query": keyword,
                "page": page
            }

            resp = requests.get(self.BASE_URL, params=params, headers=self.HEADERS, timeout=10)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            items = soup.select("ul.article > li")
            time.sleep(1)

            if not items:
                break

            for item in items:
                link_tag = item.select_one("a")
                date_tag = item.select_one("span.txt")

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

    def _fetch_article(self, url, published_at):
        resp = requests.get(url, headers=self.HEADERS, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        title = soup.select_one("h1.headline")
        content = soup.select_one("div#articletxt")

        if not title or not content:
            return None

        return {
            "title": title.text.strip(),
            "content": content.get_text(strip=True),
            "published_at": published_at,
            "url": url,
            "source": "hankyung"
        }

    def _parse_datetime(self, text: str) -> datetime:
        return datetime.strptime(text, "%Y-%m-%d %H:%M")
