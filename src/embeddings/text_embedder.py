#from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

class TextEmbedder:
    # def __init__(self):
    #     self.embeddings = HuggingFaceEmbeddings(
    #         model_name="sentence-transformers/all-MiniLM-L6-v2"
    #     )
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    

    def embed_text(self, text: str) -> list[float]:
        #return self.embeddings.embed_query(text)
        embedding = self.model.encode(text) #creating embedding for particular chunk
        return embedding.tolist()  # Convert numpy array to list for JSON serialization

    def embed_document(self, text: str) -> list[float]:
        embedding = self.model.encode(text) #creating embedding for particular chunk
        return embedding.tolist()  # Convert numpy array to list for JSON serialization
        

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        #return self.embeddings.embed_documents(texts)
        embedding = self.model.encode(texts) #creating embedding for particular chunk
        return embedding.tolist()  # Convert numpy array to list for JSON serialization
        #return [embedding.tolist() for embedding in embeddings]  # Convert numpy array to list for JSON serialization


