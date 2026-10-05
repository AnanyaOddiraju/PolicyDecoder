from pathlib import Path
from src.pipeline.ingestion_pipeline import IngestionPipeline

def test_ingestion_pipeline():
    print("1. starting test")
    pipeline = IngestionPipeline()
    print("2. pipeline created")
    file_path = Path(r"E:\AI Engineer\Pocky\Pocky_Chatbot\tests\test_data\Animal_facts.docx")
    print("Exists:", file_path.exists())
    print("Is file:", file_path.is_file())
    print("Path:", file_path)
    num_chunks = pipeline.ingest(file_path)
    print("3. ingestion completed")
    print(f"Number of chunks ingested: {num_chunks}")


    
# from src.ingestion.loader import load_files
# from src.chunking.text_chunker import chunk_document
# def test_ingestion():
#     extracted_files= load_files("E:/AI Engineer/Pocky/Pocky_Chatbot/Data")
#     chunked_files=test_chunk(extracted_files)
#     assert len(extracted_files)
#     assert(len(chunked_files))

# def test_chunk(documents):
#     all_chunks=[]
#     for document in documents:
#         chunks= chunk_document(
#             document,
#             chunk_size=1000,
#             chunk_overlap=150,
#             )
#         all_chunks.extend(chunks)
#         for i, chunk in enumerate(chunks, start=1, end=2):
#             print(f"Chunk {i}:\n{chunk}\n")
    
#     return documents
