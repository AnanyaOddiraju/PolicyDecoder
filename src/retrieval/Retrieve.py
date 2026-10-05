from src.retrieval.vector_store import VectorStore
class DocumentRetriever:
    def __init__(self,k: int = 3,):
        store = VectorStore()
        self.retriever = store.as_retriever(k=k)

    def retrieve(self,query: str):
        return self.retriever.invoke(query)