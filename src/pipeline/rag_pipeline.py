from src.embeddings.text_embedder import TextEmbedder
from src.retrieval.vector_store import VectorStore
from src.generation.llm import LLM


class RAGPipeline:
    def __init__(self):
        # Hugging Face embedding model
        self.embedder = TextEmbedder()

        # Qdrant vector database
        self.vector_store = VectorStore()

        # Gemini LLM
        self.llm = LLM()

    def ask(self, question: str, limit: int = 3) -> dict:
        """
        Run the complete RAG pipeline:

        Question
            ↓
        Hugging Face embedding
            ↓
        Qdrant similarity search
            ↓
        Retrieved chunks
            ↓
        Gemini
            ↓
        Answer + sources
        """

        # 1. Convert user's question into an embedding
        query_embedding = self.embedder.embed_text(question)

        # 2. Search Qdrant for relevant chunks
        results = self.vector_store.search(
            query_embedding=query_embedding,
            limit=limit
        )

        # 3. Extract text from retrieved chunks
        context_parts = []

        for result in results:
            text = result.payload.get("text")

            if text:
                context_parts.append(text)

        context = "\n\n".join(context_parts)

        # 4. Create prompt using retrieved context
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

        # 6. Keep source information for reference
        sources = []

        for result in results:
            sources.append({
                "id": result.id,
                "score": result.score,
                "text": result.payload.get("text", ""),
                "source": result.payload.get("source", "Unknown")
            })

        # 7. Return answer + retrieved source information
        return {
            "answer": answer,
            "sources": sources
        }