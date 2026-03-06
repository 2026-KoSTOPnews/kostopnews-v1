import os
from transformers import BertTokenizer
import onnxruntime as ort


MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../model/kobert-sentiment.onnx")
TOKENIZER_NAME = "monologg/kobert"

def load_kobert_onnx(
    model_path: str = "model/kobert-sentiment/kobert-sentiment.onnx",
    tokenizer_name: str = "monologg/kobert"
):
    tokenizer = BertTokenizer.from_pretrained(tokenizer_name)

    session = ort.InferenceSession(model_path)

    return session, tokenizer
