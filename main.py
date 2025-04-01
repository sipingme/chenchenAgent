#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: main.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-24
Last Modified Date: 2025-03-24
Description: [Description]
Version: [Version]
License: [License]
"""

import uvicorn
import config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# from agents.main.agent import Agent as ChatAgent
from chains.main_chain import MainChain
from models.file import File

config.load_config()
logger = config.logging_config()

app = FastAPI(
    title="Major and Score API",
    description="Major and Score API Docs with FastAPI",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redocs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Major and Score API Docs with FastAPI"}

@app.get("/chat")
def chat(request: Request):
    query = request.query_params.get("query", "")
    main_chain = MainChain()
    response = main_chain.executor(query)
    return response

@app.get("/add_files")
def add_files():
    logger.info("添加文档接口被访问")
    try:
        file = File()
        file.add_files()
        logger.info("文档成功添加")
        return {"message": "文档成功添加"}
    except Exception as e:
        logger.error(f"添加文档时出错：{e}")
        return {"error": "文档添加失败"}

@app.get("/query_files")
def query_files(request: Request):
    query = request.query_params.get("query", "")
    logger.info("查询文档接口被访问")
    try:
        file = File()
        response = file.query_files(query)
        logger.info("文档查询成功")
        return response.content
        
    except Exception as e:
        logger.error(f"查询文档时出错：{e}")
        return {"error": "文档查询失败"}
    
@app.get("/delete_files")
def delete_files():
    logger.info("删除文档接口被访问")
    try:
        file = File()
        file.delete_files()
        logger.info("文档删除成功")
        return {"message": "文档删除成功"}
    except Exception as e:
        logger.error(f"删除文档时出错：{e}")
        return {"error": "文档删除失败"}
    
if __name__ == "__main__":
    logger.info("启动服务器")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
