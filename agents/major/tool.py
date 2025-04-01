#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: tool.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-20
Last Modified Date: 2025-03-20
Description: [Description]
Version: [Version]
License: [License]
"""

import os
from langchain.tools import Tool
from stores.Chroma import Store as ChromaStore
class Tools:
    def __init__(self):
        self.tools = [
            Tool(
                name="大学专业的查询工具",
                func=self.major_wrapper,
                description="帮助用户查询和了解大学专业的信息。提供专业介绍、课程设置、就业前景，以及根据用户兴趣和背景进行专业推荐。适用于需要清晰和详细的专业选择指导时使用。"
            )
        ]

    def major_wrapper(self, input_text):
        chroma_store = ChromaStore(
            os.path.abspath("data"),
            os.path.abspath("databases"),
            "chroma_collection"
        )
        result = chroma_store.query_vector_store(input_text)
        return result