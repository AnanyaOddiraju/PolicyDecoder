from src.embeddings.text_embedder import TextEmbedder
from src.retrieval.vector_store import VectorStore
from src.chunking.text_chunker import chunk_document
from src.ingestion.loader import load_document
from pathlib import Path

def add_chunk_to_vector_store():
    embedder = TextEmbedder()
    store = VectorStore()

    # chunk = {
    #     "text": "This is a sample chunk of text.",
    #     "source": "test.txt",
    #     "page": None,
    # }

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

   
    for chunk_id, chunk in enumerate(chunks,start=1):
        print(f"Chunk {chunk_id}:\n{chunk}\n")
        embedding = embedder.embed_document(chunk["text"])
        store.add_chunk(chunk_id,vector=embedding, metadata=chunk)
    #embedding = embedder.embed_text(chunk["text"])
    #store.add_chunk(chunk_id=1, vector=embedding, metadata=chunk)
    #print("Chunk added to vector store with ID 1 ")

    result = store.client.retrieve(collection_name="documents", ids=[1]) 
    print(result)

def test_search_vector_store():
    embedder = TextEmbedder()
    store = VectorStore()

    user_query = "which animal helps with pollination?"
    query_embedding = embedder.embed_text(user_query)
    result_text= store.search(query_embedding=query_embedding, limit=3)
    for result in result_text:
        print("Id:", result.id)
        print("Score:", result.score)
        print("Retrieved chunk:", result.payload["text"])
        print()


