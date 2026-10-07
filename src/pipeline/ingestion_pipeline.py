from pathlib import Path
from src.ingestion.loader import load_documents
from src.chunking.item_chunker import chunk_item
from src.retrieval.vector_store import VectorStore
from src.embeddings.text_embedder import TextEmbedder

class IngestionPipeline:
    def __init__(self):
            self.embedder = TextEmbedder()
            self.store = VectorStore()
    def ingest(self,file_path: Path):
        extracted_items = load_documents(file_path)
        all_chunks = []
        
        for item in extracted_items:
            chunks= chunk_item(
                item,
                chunk_size=1000,
                chunk_overlap=150,
                )
            all_chunks.extend(chunks)
        
        for i, chunk in enumerate(all_chunks, start=1):
            print(f"Chunk {i}:\n{chunk}\n")

        # Embed the chunks
        texts = [chunk["text"] for chunk in all_chunks]
        embeddings = self.embedder.embed_document(texts)
        
        # Store the embeddings in the vector store
        for chunk_id, (chunk,embedding) in enumerate(zip(all_chunks,embeddings),start=1):
            self.store.add_chunk(chunk_id=chunk_id, vector=embedding, metadata=chunk)
        return len(all_chunks)
