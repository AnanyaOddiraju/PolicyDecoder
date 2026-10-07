from pathlib import Path
from src.ingestion.loader import load_documents
from src.chunking.item_chunker import chunk_item
def test_chunking():
    file_path = Path("D:/Policy_Decoder/PolicyDecoder/Data/Brochures")
    extracted_items = load_documents(file_path)
    print(extracted_items[0])
    assert len(extracted_items) > 0, "No documents were extracted"
    all_chunks = []
    for item in extracted_items:
        chunks = chunk_item(
            item,
            chunk_size=500,
            chunk_overlap=75,
        )
        print(
            f"\nSource: {item['source']}"
            f"\nType: {item['type']}"
            f"\nPage: {item.get('page')}"
        )
        all_chunks.extend(chunks)
    for chunk in all_chunks:
            print(f"Chunk {chunk['chunk_index']}:\n{chunk}\n")