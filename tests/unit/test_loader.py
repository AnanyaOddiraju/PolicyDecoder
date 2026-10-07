from pathlib import Path
from src.ingestion.loader import load_documents
def test_loader():
    file_path = Path("D:/Policy_Decoder/PolicyDecoder/Data/House/ICICI home.pdf")
    extracted_items = load_documents(file_path)
    print(extracted_items[0])