#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: config.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-24
Last Modified Date: 2025-03-24
Description: [Description]
Version: [Version]
License: [License]
"""

import os
import logging
import coloredlogs
from dotenv import load_dotenv

def load_config():
    load_dotenv()

    logger = logging.getLogger(__name__)
    coloredlogs.install(level='INFO', logger=logger)
    
    logger.info("成功加载环境变量")
    
    model_name = os.environ.get("MODEL_NAME")
    if model_name:
        logger.info(f"使用模型名称: {model_name}")

        os.environ["DEEPSEEK_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
        os.environ["DEEPSEEK_API_BASE"] = os.getenv("DEEPSEEK_API_BASE")
        os.environ["DEEPSEEK_API_MODEL"] = os.getenv("DEEPSEEK_API_MODEL")
        
        os.environ["ZHIPUAI_API_KEY"] = os.getenv("ZHIPUAI_API_KEY")
        os.environ["ZHIPUAI_API_BASE"] = os.getenv("ZHIPUAI_API_BASE")
        os.environ["ZHIPUAI_API_MODEL"] = os.getenv("ZHIPUAI_API_MODEL")
        os.environ["ZHIPUAI_API_EMBEDDING"] = os.getenv("ZHIPUAI_API_EMBEDDING")

        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

        os.environ["HF_ENDPOINT"] = os.getenv("HF_ENDPOINT")

        logger.info("环境变量已成功设置")
    else:
        logger.error("请检查环境变量设置")

    os.environ["MODEL_NAME"] = model_name


def logging_config():
    logger = logging.getLogger(__name__)
    return logger