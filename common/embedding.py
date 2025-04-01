import os
import torch
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

class Embedding:
    def __init__(self):
        self.model_name = os.environ.get("MODEL_NAME")
        if self.model_name == "ZHIPUAI-":
            self.embedding = ZhipuAIEmbeddings()
        elif self.model_name == "DEEPSEEK":
            self.embedding = ZhipuAIEmbeddings()
        else:
            model_name = "BAAI/bge-m3"
            model_kwargs = {
                "device": "cuda" if torch.cuda.is_available() else "cpu",
                "from_tf": True
            }
            encode_kwargs = {"normalize_embeddings": True}
            self.embedding = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )