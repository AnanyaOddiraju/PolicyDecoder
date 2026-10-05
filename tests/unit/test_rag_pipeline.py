from src.pipeline.rag_pipeline import RAGPipeline

def test_rag_pipeline():
    pipeline = RAGPipeline()

    user_query = "Give 3 animals that contribute to pollination"
    response = pipeline.ask(user_query)

    print("\nRAG Pipeline response:")
    print(response["answer"])
    print("\nSources:")

    for s in response["sources"]:
        print(f"ID: {s['id']}")
        print(f"Score: {s['score']}")
        print(f"Source: {s['source']}")
        print(f"Text: {s['text']}")
        print("-" * 50)
    assert response["answer"]
    assert response["sources"]