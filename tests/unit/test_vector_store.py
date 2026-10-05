from src.retrieval.vector_store import VectorStore

def test_vector_store():
    store = VectorStore()
    print(store.client.get_collection("documents"))