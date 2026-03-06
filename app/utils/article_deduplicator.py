import re
import hashlib
from typing import List, Dict


class ArticleDeduplicator:
    def __init__(self):
        self._seen_urls: set[str] = set()
        self._seen_titles: set[str] = set()

    def deduplicate(self, articles: List[Dict]) -> List[Dict]:
        unique_articles = []

        for article in articles:
            if self._is_duplicate(article):
                continue

            self._mark_seen(article)
            unique_articles.append(article)

        return unique_articles

    def _is_duplicate(self, article: Dict) -> bool:
        url = article.get("url")
        title = article.get("title")

        if url and url in self._seen_urls:
            return True

        if title:
            title_hash = self._hash_title(title)
            if title_hash in self._seen_titles:
                return True

        return False

    def _mark_seen(self, article: Dict):
        if article.get("url"):
            self._seen_urls.add(article["url"])

        if article.get("title"):
            self._seen_titles.add(self._hash_title(article["title"]))

    @staticmethod
    def _hash_title(title: str) -> str:
        normalized = ArticleDeduplicator._normalize_title(title)
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    @staticmethod
    def _normalize_title(title: str) -> str:
        title = title.lower()
        title = re.sub(r"\s+", " ", title)
        title = re.sub(r"[^\w\s]", "", title)
        return title.strip()
