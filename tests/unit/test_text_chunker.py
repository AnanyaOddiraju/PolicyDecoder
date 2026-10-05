from src.chunking.text_chunker import chunk_document
from src.ingestion.loader import load_document
from pathlib import Path


def test_chunk_text():
    file_path = Path(
        r"E:\AI Engineer\Pocky\Pocky_Chatbot\tests\test_data\Animal_facts.docx"
    )

    documents = load_document(file_path)

    chunks = []

    for document in documents:
        chunks.extend(
            chunk_document(
                document,
                chunk_size=500,
                chunk_overlap=100
            )
        )

    for i, chunk in enumerate(chunks, start=1):
        print(f"Chunk {i}:\n{chunk}\n")

    assert len(chunks) > 0