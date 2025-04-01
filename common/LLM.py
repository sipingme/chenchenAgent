#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: LLM.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-24
Last Modified Date: 2025-03-24
Description: [Description]
Version: [Version]
License: [License]
"""

import os
from langchain_community.chat_models import ChatZhipuAI
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
class CustomLLM:
    def __init__(self, temperature=0):
        model_name = os.environ.get("MODEL_NAME")
        
        if model_name == "ZHIPUAI":
            self.llm = ChatZhipuAI(
                temperature=temperature
            )
            # self.llm = ChatOpenAI(
            #     temperature=temperature,
            #     model_name="gpt-3.5-turbo"
            # )
        elif model_name == "DEEPSEEK":
            self.llm = ChatDeepSeek(
                temperature=temperature,
                model=os.environ.get("DEEPSEEK_API_MODEL")
            )

    def initialize(self, data=None):
        return self.llm