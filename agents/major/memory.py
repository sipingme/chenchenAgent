#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: memory.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-20
Last Modified Date: 2025-03-20
Description: [Description]
Version: [Version]
License: [License]
"""

import os
import config
from langchain.memory import ConversationTokenBufferMemory, ConversationBufferWindowMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.prompts import ChatPromptTemplate
from .prompt import Prompt as MajorPrompt

logger = config.logging_config()

class Memory:
    def __init__(self):
        self.memory_key = "history"
        self.llm = self.get_llm(os.environ.get("MODEL_NAME"))
        logger.info("Memory已使用模型初始化: %s", os.environ.get("MODEL_NAME"))

    def get_llm(self, model_name):
        logger.info("获取语言模型，模型名称: %s", model_name)
        if model_name == "ZHIPUAI":
            logger.info("使用ChatZhipuAI模型。")
            return ChatZhipuAI()
        logger.warning("未知的模型名称: %s", model_name)
        return None

    def get_conversation_token_buffer_memory(self):
        conversation_token_buffer_memory = ConversationTokenBufferMemory(
            chat_memory=self.get_redis_chat_message_history(),
            llm=self.llm,
            memory_key=self.memory_key,
            human_prefix="user",
            ai_prefix="system",
            max_token_limit=128,
            return_messages=True
        )
        return conversation_token_buffer_memory

    def get_conversation_buffer_window_memory(self):
        conversation_buffer_window_memory = ConversationBufferWindowMemory(k=2)
        return conversation_buffer_window_memory
    
    def get_redis_chat_message_history(self):
        logger.debug("获取RedisChatMessageHistory。")
        try:
            redis_chat_message_history = RedisChatMessageHistory(
                url="redis://redis:6379/0",
                session_id=self.memory_key
            )
            stored_messages = redis_chat_message_history.messages
            logger.info("获取到 %d 条存储的消息。", len(stored_messages))

            if len(stored_messages) > 2:
                concatenated_messages = "".join(
                    f"{type(message).__name__}: {message.content}" for message in stored_messages
                )
                logger.info("用于摘要的连接消息: %s", concatenated_messages)
                summary = self.summary_chain(concatenated_messages)
                redis_chat_message_history.clear()
                redis_chat_message_history.add_message(summary)
                logger.info("消息已总结并存储。")
                return redis_chat_message_history
            else:
                return redis_chat_message_history
        except Exception as e:
            logger.error("获取RedisChatMessageHistory失败: %s", str(e))
            return None

    def summary_chain(self, stored_messages):
        major_prompt = MajorPrompt()
        system_prompt = major_prompt.generate_template()
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt + "\n这是一段你和用户的对话记忆，对其进行总结摘要，然后回答用户的问题："),
            ("user", "{input}")
        ])
        chain = prompt | self.llm
        summary = chain.invoke({"input": stored_messages})
        logger.info("正在总结消息。")
        return summary