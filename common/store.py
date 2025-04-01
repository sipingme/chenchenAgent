import os
from langchain_chroma import Chroma
from .embedding import Embedding

class Store:
    def __init__(self):
        db_path = os.getenv("DB_PATH")
        collection_name = os.getenv("COLLECTION_NAME")
        embedding_function = Embedding().embedding
        self.chroma = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_function,
            persist_directory=db_path
        )