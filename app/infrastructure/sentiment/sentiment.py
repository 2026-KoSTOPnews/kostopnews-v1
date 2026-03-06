import numpy as np
from typing import List, Dict, Tuple

# 회귀
class SentimentAnalyzer:
    """
    KoBERT 회귀 모델 기반 감정 분석기
    - 하루 / 유저 단위 모두 요약 뉴스 리스트를 입력으로 감정 분석
    - 모델 출력 범위: 0 ~ 1
    """

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def analyze(self, text: str) -> Tuple[str, float]:
        """
        하루 요약 뉴스 리스트를 받아 평균 score 계산 후 sentiment 분류
        """
        if text == "수집된 기사가 없습니다.":
            return "NEUTRAL", 0.5  # 뉴스 없으면 중립

        scores = []
        for summary in text:
            inputs = self.tokenizer(
                summary,
                truncation=True,
                padding=True,
                max_length=256,
                return_tensors="np"
            )
            outputs = self.model.run(
                None,
                {
                    "input_ids": inputs["input_ids"],
                    "attention_mask": inputs["attention_mask"]
                }
            )
            score = float(outputs[0][0][0])
            score = max(0.0, min(score, 1.0))  # clamp 0~1
            scores.append(score)

        text_score = float(np.mean(scores))

        # Threshold 기준
        if text_score < 0.45:
            label = "NEGATIVE"
        elif text_score > 0.62:
            label = "POSITIVE"
        else:
            label = "NEUTRAL"

        return label, text_score



# 분류
# class SentimentAnalyzer:
#     """
#     KoBERT ONNX 모델 기반 감정 분석기
#     입력: 하루 요약 텍스트 (str)
#     출력: 감정 label (POSITIVE / NEGATIVE)
#     """
#
#     def __init__(self, model, tokenizer):
#         self.model = model
#         self.tokenizer = tokenizer
#         self.label_map = {
#             0: "NEGATIVE",
#             1: "POSITIVE"
#         }
#
#     def analyze(self, text: str) -> tuple[str, float]:
#         inputs = self.tokenizer(
#             text,
#             truncation=True,
#             padding=True,
#             max_length=256,
#             return_tensors="np"
#         )
#
#         outputs = self.model.run(
#             None,
#             {
#                 "input_ids": inputs["input_ids"],
#                 "attention_mask": inputs["attention_mask"]
#             }
#         )
#
#         logits = outputs[0]
#
#         # softmax
#         exp = np.exp(logits - np.max(logits, axis=1, keepdims=True))
#         probs = exp / np.sum(exp, axis=1, keepdims=True)
#
#         pred_label = int(np.argmax(probs, axis=1)[0])
#         score = float(np.max(probs))
#
#         print("pred_label:", pred_label)
#         print("score:", score)
#         print("probs:", probs)
#         score = float(np.max(probs))
#
#         return self.label_map[pred_label], score
