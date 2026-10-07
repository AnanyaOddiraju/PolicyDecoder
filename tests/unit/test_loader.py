from pathlib import Path
from src.ingestion.loader import load_document
def test_loader():
  file_path = Path("D:/Policy_Decoder/PolicyDecoder/Data/House/ICICI home.pdf")
  loaded_files = load_document(file_path)
  print(loaded_files[0])