#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: Prompts.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-25
Last Modified Date: 2025-03-25
Description: [Description]
Version: [Version]
License: [License]
"""

from langchain.prompts import ChatPromptTemplate
class CustomPrompt:
    def __init__(self):
        pass

    def optimize_prompt(self, data=None):
        """
        Optimize a question using contextual information to improve the accuracy of responses.

        Parameters:
        - data: A dictionary containing 'context' and 'question'.

        Returns:
        - An optimized question template designed to supplement missing information, clarify ambiguity, and maintain professional terminology.
        """
        return ChatPromptTemplate.from_template("""
            根据上下文优化问题以提高回答准确性：
            上下文：{context}

            原始问题：{question}
            优化策略：
            1. 补充缺失的关键信息
            2. 明确模糊指代
            3. 保持专业术语
            优化后的问题：""")

    def agent_prompt(self, data=None):
        """
        Generate a prompt template for an intelligent assistant capable of leveraging tools and knowledge.

        Parameters:
        - data: A dictionary containing 'input' and 'agent_scratchpad'.

        Returns:
        - A structured message prompt that sets the context for the assistant to respond effectively.
        """
        return ChatPromptTemplate.from_messages([
            ("system", "你是能综合使用工具和知识的专业助手。"),
            ("user", "{input}"),
            ("assistant", "{agent_scratchpad}")
        ])

    def answer_prompt(self, data=None):
        """
        Create an answer prompt to systematically address user questions using relevant context.

        Parameters:
        - data: A dictionary containing 'context' and 'optimized_question'.

        Format for answering:
        - Core conclusion: Summarized in up to 50 words.
        - Key steps analysis: Breakdown of the process or reasoning.
        - Additional explanation: Any further information if applicable.

        Returns:
        - A structured template for providing comprehensive answers based on the context.
        """
        return ChatPromptTemplate.from_template("""
            综合以下资源回答问题：
            相关上下文：{context}

            问题：{optimized_question}
            答案：""")