#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: MajorPlanTool.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-25
Last Modified Date: 2025-03-25
Description: This module provides a tool for retrieving university enrollment plans and details about college majors.
Version: [Version]
License: [License]
"""

from langchain.tools import Tool
from stores.Chroma import Store as ChromaStore
from common.Prompt import CustomPrompt
from common.LLM import CustomLLM
class MajorPlanTool:
    def __init__(self):
        """
        Initializes the MajorPlanTool class, setting up the tool for major plan retrieval and initializing the ChromaStore.

        Sets up:
        - self.tool: A tool instance for querying major plans.
        - self.chroma_store: An instance of ChromaStore for data retrieval.
        """
        self.tool = Tool(
            name="MajorPlanTool",
            func=self.major_plan_wrapper,
            description=(
                "该工具用于检索大学的招生计划和学院的专业设置。"
                "它提供详细的专业信息，帮助用户了解具体专业的课程安排、入学要求和其他相关内容。"
                "用户可以利用此工具获取全面的专业设置信息，以支持教育规划和决策。"
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
            return None

    def major_plan_wrapper(self, input_text):
        """
        Wrapper function for querying university enrollment plans and college major details.

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
