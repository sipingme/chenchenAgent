#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: file.py
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
from langchain_community.document_loaders import UnstructuredExcelLoader, Docx2txtLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from stores.Chroma import Store as ChromaStore

logger = config.logging_config()
class File:
    def __init__(self):
        self.data_path = os.getenv("DATA_PATH")
        self.db_path = os.getenv("DB_PATH")
        self.collection_name = os.getenv("COLLECTION_NAME")
        self.split_texts_list = []

    def query_files(self, query):
        logger.info(f"查询文本: {query}")
        if not query:
            logger.warning("未指定查询文本")
            return None
        
        logger.info("查询向量存储")
        chroma_store = ChromaStore()
        result = chroma_store.query_vector_store(query)
        logger.info(f"查询结果: {result}")
        return result
    
    def delete_files(self):
        logger.info("删除文件")
        self.split_texts_list = []
        return self.save_file()

    def add_files(self):
        if not self.data_path:
            logger.warning("未指定目录路径")
            return None
        
        loaders = {
            "pdf": PyPDFLoader,
            "docx": Docx2txtLoader,
            "xlsx": UnstructuredExcelLoader
        }
        
        logger.info(f"处理目录: {self.data_path}")
        for filename in os.listdir(self.data_path):
            file_path = os.path.join(self.data_path, filename)
            if os.path.isfile(file_path):
                self.process_file(file_path, filename, loaders)
            else:
                logger.info(f"跳过非文件项: {filename}")

        return self.save_file()
    
    def process_file(self, file_path, filename, loaders):
        file_extension = filename.split(".")[-1].lower()
        loader_class = loaders.get(file_extension)

        if loader_class:
            try:
                logger.info(f"加载文件 '{filename}'，扩展名为 '{file_extension}'")
                loader = loader_class(file_path)
                document_text = loader.load()
                if document_text:
                    logger.info(f"成功从 '{filename}' 加载文本")
                    self.split_file_texts(document_text)
                else:
                    logger.warning(f"'{filename}' 中未找到文本")
            except Exception as e:
                logger.error(f"加载 '{file_extension}' 文件 '{filename}' 时出错：{e}")
        else:
            logger.info(f"不支持的文件扩展名：'{file_extension}'，文件名为 '{filename}'")

    def split_file_texts(self, document_text):
        logger.info("分割文档文本")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.split_texts_list.extend(text_splitter.split_documents(document_text))

    def save_file(self):
        logger.info(f"创建向量存储：{self.collection_name}")
        chrmoa_store = ChromaStore()
        create_vector_store = chrmoa_store.create_vector_store(self.split_texts_list)
        logger.info(f"向量存储 '{self.collection_name}' 创建成功")
        return create_vector_store