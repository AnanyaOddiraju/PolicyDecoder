from unittest import result
from src.embeddings.text_embedder import TextEmbedder
from src.retrieval.vector_store import VectorStore
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




# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_groq import chatGroq
# from langchain.chains import RetreivalQA
# from langchain.prompts import PromptTemplate
# import os
# from dotenv import load_dotenv

# load_dotenv()
# def create_vectorstorage(chunks):
#     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     vectors = Chroma.from_documents(chunks, embeddings)
#     return vectors