from src.embeddings.text_embedder import TextEmbedder
import pytest
#pytest.importorskip("torch")

embedder = TextEmbedder()
text = "This is a sample text for embedding test."
texts = ["This is the first sample text for embedding test.", "This is the second sample text for embedding test."]

def test_text_embedder():
    print("Embeddings for Text:")
    embedding = embedder.embed_text(text)
    print(f"Length of embedding: {len(embedding)}")
    print(f"First 5 elements of embedding: {embedding[:5]}")
    assert isinstance(embedding, list)
    assert len(embedding) > 0

def test_document_embedder():
    print("Embeddings for Documents:")
    embeddings = embedder.embed_documents(texts)
    print(f"Number of chunks: {len(embeddings)}")
    print(f"Length of each embedding: {len(embeddings[0])}")
    assert isinstance(embeddings[0], list)
    assert len(embeddings[0]) > 0
    for text, embedding in zip(texts, embeddings):
        print(f"Text: {text}")
        print(f"Embedding Length: {len(embedding)}")
        print(f"First 5 elements of embedding: {embedding[:5]}")
        