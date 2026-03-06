import os
from dotenv import load_dotenv
from typing import List, Dict

from google import genai


class NewsSummarizer:
    """
    기업 뉴스 요약기
    """

    def summarize(self, articles: List[Dict]) -> str:
        """
        articles:
        [
          {
            "title": str,
            "content": str,
            ...
          }
        ]
        """

        if not articles:
            return "수집된 기사가 없습니다."

        merged_text = self._merge_articles(articles)

        prompt = f"""
                        다음은 특정 기업과 관련된 뉴스 기사 모음입니다.
                        뉴스 기사들을 핵심 이슈 위주로 요약하고, 중복되는 내용은 제거하고,
                        5~10줄로 요약하도록 노력하되, 넘어간다면 최대 20줄을 넘지 않도록 요약해 주시기 바랍니다.
                        
                        {merged_text}
                        """

        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        print(response)

        summary = response.text

        return summary

    def _merge_articles(self, articles: List[Dict]) -> str:
        """
        기사들을 하나의 텍스트로 병합
        """
        texts = []

        for idx, article in enumerate(articles, start=1):
            title = article.get("title", "")
            content = article.get("content", "")
            texts.append(f"[기사 {idx}]\n제목: {title}\n내용: {content}")

        return "\n\n".join(texts)
