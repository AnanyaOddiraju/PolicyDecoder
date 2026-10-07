from pathlib import Path
from src.ingestion.document_extractor import extract_docx, extract_txt,extract_pdf

def load_document(path: str | Path) -> list[dict]:
   
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Data directory not found: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Expected a file: {file_path}")
    
    extension = file_path.suffix.lower()

    if extension ==".pdf":
        return extract_pdf(file_path)
    elif extension == ".docx":
        return extract_docx(file_path)    
    elif extension in [".txt", ".md"]:
        return extract_txt(file_path) 
    raise ValueError(f"Unsupported file type: {extension}. Supported types are: .pdf, .docx, .txt, .md")

def load_documents(path : str | Path) -> list[dict]:
  path = Path(path)
  if not path.exists():
    raise FileNotFoundError(f"Data Directory Not Found: {path}")
  all_files=[]
  
  if path.is_file():
    return load_document(path)
  if path.is_dir():
    for file_path in path.rglob("*"):
      if not file_path.is_file():
        continue
      try:
        extracted_items = load_document(file_path)
        all_files.extend(extracted_items)

      except ValueError as exc:
        print(f"Skipping {file_path}: {exc}")
  return all_files