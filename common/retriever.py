from .store import Store

class Retriever:
    def __init__(self):
        self.store = Store().chroma
        self.as_retriever = self.store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold":.1, "k":1}
        )