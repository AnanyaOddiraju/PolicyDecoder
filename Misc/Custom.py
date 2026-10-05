#Embedding using sentence transformer
from sentence_transformers import SentenceTransformer

class TextEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        embedding = self.model.encode(text) #creating embedding for particular chunk
        return embedding.tolist()  # Convert numpy array to list for JSON serialization

    def embed_document(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts) #creating embedding for set of chunks at once
        return embeddings.tolist()  # Convert numpy array to list for JSON serialization
        #return [embedding.tolist() for embedding in embeddings]  # Convert numpy array to list for JSON serialization

#Custom Qdrant vector store add/search
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

class VectorStore:
    def __init__(self, collection_name: str = "documents"):
        self.client = QdrantClient(path="./qdrant_data")
        self.collection_name = collection_name
        self._create_collection()

    def _create_collection(self):
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
    def add_chunk(self, chunk_id: int, vector: list[float], metadata: dict):
        point = PointStruct(id=chunk_id, vector=vector, payload=metadata)
        self.client.upsert(collection_name=self.collection_name, points=[point])
    def search(self,query_embedding:list[float],limit: int =3):
        results = self.client.query_points(collection_name=self.collection_name, query=query_embedding, limit=limit, with_payload=True)
        return results.points

#Ingestion - loader.py
#Decides which loader to use based on the file type
from pathlib import Path
from .document_extractor import (extract_text_from_docx, extract_text_from_pdf, extract_text_from_txt)

#file_path is expected to be a string dtype and function must return list data type (which has json ex: [{page :1 }, {page:2},{page:3}])
def load_document(file_path : str) -> list[dict]:
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension ==".pdf":
        return extract_text_from_pdf(file_path)
    elif extension in [".docx", ".doc"]:
        return extract_text_from_docx(file_path)    
    elif extension in [".txt", ".md"]:
        return extract_text_from_txt(file_path) 
    raise ValueError(f"Unsupported file type: {extension}. Supported types are: .pdf, .docx, .doc, .txt, .md")

#Ingestion pipeline
from src.ingestion.loader import load_document
from src.chunking.text_chunker import chunk_document
from src.embeddings.text_embedder import TextEmbedder
from src.retreival.vector_store import VectorStore

class IngestionPipeline:
    def __init__(self):
        self.embedder = TextEmbedder()
        self.vector_store = VectorStore()

    def ingest(self, file_path: str):
        # Load the document
        documents = load_document(file_path)
        print("Document length:", len(documents[0]["text"]))
        # Chunk the document
        all_chunks = []
        for document in documents:
            chunks = chunk_document(document, chunk_size=500, chunk_overlap=100)
            all_chunks.extend(chunks)
            for i, chunk in enumerate(chunks, start=1):
                print(f"Chunk {i}:\n{chunk}\n")
        # Embed the chunks
        texts = [chunk["text"] for chunk in all_chunks]
        embeddings = self.embedder.embed_document(texts)

        # Store the embeddings in the vector store
        for chunk_id, (chunk,embedding) in enumerate(zip(all_chunks,embeddings),start=1):
            self.vector_store.add_chunk(chunk_id=chunk_id, vector=embedding, metadata=chunk)
        return len(all_chunks)

#Rag pipeline
from unittest import result
from src.embeddings.text_embedder import TextEmbedder
from src.retreival.vector_store import VectorStore
from src.generation.llm import LLM


class RAGPipeline:
    def __init__(self):
        self.embedder = TextEmbedder()
        self.vector_store = VectorStore()
        self.llm = LLM()

    def ask(self, question: str, limit: int = 3) -> str:

        # 1. Convert user's question into an embedding
        query_embedding = self.embedder.embed_text(question)

        # 2. Search Qdrant for relevant chunks
        results = self.vector_store.search(
            query_embedding=query_embedding,
            limit=limit
        )

        # 3. Extract text from retrieved chunks
        context = "\n\n".join(
            result.payload["text"]
            for result in results
        )

        # 4. Create prompt containing retrieved context
        prompt = f"""
You are Pocky, a helpful Multimodal RAG chatbot.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

        # 5. Send context + question to Gemini
        answer = self.llm.generate(prompt)

        
        #6. Keep source information for reference
        sources=[]
        for result in results:
            #print("SOURCE FROM PAYLOAD:", result.payload.get("source"))
            sources.append({
                "id": result.id,
                "score": result.score,
                "text": result.payload["text"],
                "source": result.payload.get("source", "Unknown")
            })
        # for result in results:
        #     print("PAYLOAD:", result.payload)
        return {
            "answer": answer,
            "sources": sources
        }

#llm.py
import os
from dotenv import load_dotenv
from google import genai


class LLM:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.8-flash"

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text