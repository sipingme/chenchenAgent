#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: AnnualScoresTool.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-25
Last Modified Date: 2025-03-25
Description: This module provides a tool for querying university admission score lines, including details for different majors and batches.
Version: [Version]
License: [License]
"""

from langchain.tools import Tool
from stores.Chroma import Store as ChromaStore
from common.Prompt import CustomPrompt
from common.LLM import CustomLLM
class AnnualScoresTool:
    def __init__(self):
        """
        Initializes the AnnualScoresTool class, setting up the tool for admission score retrieval and initializing the ChromaStore.

        Sets up:
        - self.tool: A tool instance for querying admission scores.
        - self.chroma_store: An instance of ChromaStore for data retrieval.
        """
        self.tool = Tool(
            name="AnnualScoresTool",
            func=self.search_score_wrapper,
            description=(
                "该工具旨在查询并提供全面的大学录取分数线信息。"
                "它提供每个专业的具体分数线，包括不同录取批次和要求的变化。"
                "用户可以利用此工具获取最新且准确的分数数据，以帮助做出有关大学申请的明智决策。"
            )
        )
        self.chroma_store = self._initialize_chroma_store()
        self.prompt = CustomPrompt().answer_prompt()
        self.llm = CustomLLM().initialize()
        
    def _initialize_chroma_store(self):
        """
        Attempts to initialize the ChromaStore.

        Returns:
        - ChromaStore: A ChromaStore instance if successful, otherwise None.
        """
        try:
            return ChromaStore()
        except Exception as e:
            print(f"Chroma初始化失败: {e}")
            return None

    def search_score_wrapper(self, input_text):
        """
        Wrapper function for querying university admission scores.

        Parameters:
        - input_text (str): The input text containing the query details.

        Returns:
        - str: The query result (currently returns an empty string, should be implemented).
        """
        retriever = self.chroma_store.retrieve_vector_store()
        _content = ""
        context = retriever.invoke(input_text)
        for i in context:
            _content += i.page_content

        messages = self.prompt.format_messages(
            context=_content,
            optimized_question=input_text
        )
        results = self.llm.invoke(messages)
        return results