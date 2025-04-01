#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: agent.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-20
Last Modified Date: 2025-03-20
Description: [Description]
Version: [Version]
License: [License]
"""

import langchain
import config
from common.PromptTemplate import CustomPromptTemplate
from common.LLMChain import CustomLLMChain
from common.LLMSingleActionAgent import CustomLLMSingleActionAgent
from common.OutputParser import CustomOutputParser
from common.AgentExecutor import CustomAgentExecutor
from .prompt import Prompt as MajorPrompt
from .tool import Tools as MajorTools
from .memory import Memory as MajorMemory

logger = config.logging_config()
class Agent:
    def __init__(self):
        self.name = "Major Agent"
        
        major_tools = MajorTools()
        self.tools = major_tools.tools
        tool_names = [tool.name for tool in self.tools]
        logger.info(f"工具初始化完成: {tool_names}")

        prompt_template = CustomPromptTemplate(
            template=MajorPrompt.generate_template(),
            tools=self.tools,
            input_variables=["input", "intermediate_steps", "history"]
        )
        logger.info("提示模板创建完成")

        custom_llm_chain = CustomLLMChain(
            prompt=prompt_template,
            temperature=0
        )
        llm_chain = custom_llm_chain.initialize()
        logger.info("LLM链初始化完成")

        custom_llm_single_action_agent = CustomLLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=CustomOutputParser(),
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )
        self.agent = custom_llm_single_action_agent.initialize()
        logger.info("单动作代理初始化完成")

        major_memory = MajorMemory()
        self.memory = major_memory.get_conversation_token_buffer_memory()
        logger.info("搜索记录初始化完成")

    def run_agent(self, user_input):
        logger.info(f"执行代理，用户输入: {user_input}")
        langchain.debug = True
        custom_agent_executor = CustomAgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            return_intermediate_steps=True,
            verbose=True
        )
        agent_executor = custom_agent_executor.execute()

        logger.info("代理执行器被调用")
        try:
            result = agent_executor.invoke(user_input)
            logger.info(f"代理执行结果: {result}")
            return result
        except Exception as e:
            logger.error(f"代理执行过程中发生错误: {e}")
            result = None