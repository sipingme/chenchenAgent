#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: main_chain.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-24
Last Modified Date: 2025-03-24
Description: [Description]
Version: [Version]
License: [License]
"""

from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.output_parser import StrOutputParser
from common.RAG import CustomRAG
from common.Prompt import CustomPrompt
from common.LLM import CustomLLM
from common.CreateToolCallingAgent import CustomCreateToolCallingAgent

class MainChain:
    def __init__(self):
        self.rag = CustomRAG()
        self.prompt = CustomPrompt()
        self.llm = CustomLLM()
        self.agent = CustomCreateToolCallingAgent(0, self.prompt.agent_prompt()).initialize()

    def executor(self, question):
        chain = (
            RunnablePassthrough.assign(
                context=lambda x: self.rag.retrieve(x["question"])
            )
            .assign(
                optimized_question=RunnablePassthrough.assign(
                    ctx=lambda x: x["context"],
                    q=lambda x: x["question"]
                )
                | self.prompt.optimize_prompt
                | self.llm.initialize
                | StrOutputParser()
            )
            .assign(
                agent_result=lambda x: self.agent.invoke(
                    {"input": x["optimized_question"]}
                )
            )
            .assign(
                rag_answer=self.prompt.answer_prompt()
                | self.llm.initialize
                | StrOutputParser()
            )
            .assign(
                final_answer=RunnableLambda(self.route_based_on_tools)
            )
            # .assign(
            #     storage_result=lambda x: redis_client.set(
            #         x["question"], 
            #         x["final_answer"]
            #     )
            # )
        )
        response = chain.invoke({
            "question": question
        })
        return response["final_answer"]
    
    def route_based_on_tools(self, x):
        if len(x["agent_result"]["intermediate_steps"]) > 0:
            return x["agent_result"]["output"]
        return x["rag_answer"]