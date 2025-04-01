#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: RAG.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-25
Last Modified Date: 2025-03-25
Description: This module utilizes Retrieval-Augmented Generation (RAG) to optimize and retrieve relevant documents based on a question.
Version: [Version]
License: [License]
"""

# Import necessary modules and configurations
import config
from stores.Chroma import Store as ChromaStore
from common.LLM import CustomLLM

# Initialize logging based on configuration
logger = config.logging_config()

class CustomRAG:
    def __init__(self):
        """
        Initializes the CustomRAG class with components for retrieval and language model processing.
        
        - self.retriever: Utilizes ChromaStore to retrieve relevant documents.
        - self.llm: Initializes a custom language model with a specified temperature.
        """
        self.retriever = ChromaStore().retrieve_vector_store()
        self.llm = CustomLLM(temperature=0).initialize()

    def retrieve(self, question: str) -> list:
        """
        Retrieves documents relevant to the given question using vector store retrieval.

        Parameters:
        - question (str): The question to base document retrieval on.

        Returns:
        - list: A list of relevant documents.
        """
        return self.retriever.invoke(question)

    # def retrieve(self, question: str) -> str:
    #     """
    #     Retrieves and concatenates the content of the top relevant documents.

    #     Parameters:
    #     - question (str): The question to base document retrieval on.

    #     Returns:
    #     - str: Concatenated page content from the top relevant documents.
    #     """
    #     docs = self.retriever.invoke(question)
    #     return "\n".join(doc.page_content for doc in docs[:3])