#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: Chroma.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-24
Last Modified Date: 2025-03-24
Description: [Description]
Version: [Version]
License: [License]
"""

import os
import config
import torch
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

logger = config.logging_config()
class Store:
    def __init__(self):
        self.db_path = os.getenv("DB_PATH")
        self.collection_name = os.getenv("COLLECTION_NAME")
        self.model_name = os.environ.get("MODEL_NAME")
        self.chroma = Chroma(
            persist_directory=self.db_path,
            embedding_function=self.get_embeddings(),
            collection_name=self.collection_name
        )

    def create_vector_store(self, split_texts_list):
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
            logger.info(f"创建目录: {self.db_path}")

        if self.chroma:
            try:
                self.chroma.add_documents(split_texts_list, collection_name=self.collection_name)
                logger.info("文档已成功添加并保存")
            except Exception as e:
                logger.error(f"添加文档时发生错误: {e}")
        return self.chroma
    
    def query_vector_store(self, query_text):

        return ""

    def retrieve_vector_store(self):
        return self.chroma.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold":.1, "k":1}
        )

    def get_embeddings(self):
        if self.model_name == "ZHIPUAI-":
            self.embedding = ZhipuAIEmbeddings()
            return self.embedding
        elif self.model_name == "DEEPSEEK":
            self.embedding = ZhipuAIEmbeddings()
            return self.embedding
        else:
            model_name = "BAAI/bge-m3"
            model_kwargs = {"device": "cuda" if torch.cuda.is_available() else "cpu"}
            encode_kwargs = {"normalize_embeddings": True}
            self.embedding = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )
        return self.embedding