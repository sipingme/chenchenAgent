#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: CreateToolCallingAgent.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-25
Last Modified Date: 2025-03-25
Description: This module sets up an agent capable of calling tools using a specified language model and prompt.
Version: [Version]
License: [License]
"""

from langchain.agents import AgentExecutor, create_tool_calling_agent
from common.LLM import CustomLLM
from common.Tools import CustomTools

class CustomCreateToolCallingAgent:
    def __init__(self, temperature, prompt):
        """
        Initializes the CustomCreateToolCallingAgent class.

        Parameters:
        - temperature (float): Temperature setting for the language model, influencing response variability.
        - prompt (str): Initial prompt to guide agent behavior.

        Sets up:
        - llm: A customized language model initialized with the specified temperature.
        - tools: A list of initialized tools for the agent to utilize.
        - agent_executor: An agent executor configured to execute actions using the agent and tools.
        """
        llm = CustomLLM(temperature=temperature).initialize()
        tools = CustomTools().initialize()
        agent = create_tool_calling_agent(llm, tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            return_intermediate_steps=True,
            verbose=True
        )

    def initialize(self):
        """
        Returns the initialized agent executor.

        Returns:
        - AgentExecutor: The configured agent executor ready to perform actions.
        """
        return self.agent_executor