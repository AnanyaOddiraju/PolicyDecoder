from pathlib import Path
from src.ingestion.document_extractor import extract_docx, extract_txt,extract_pdf

def load_document(path: str | Path) -> list[dict]:
   
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Data directory not found: {file_path}")

    extension = file_path.suffix.lower()

    if extension ==".pdf":
        return extract_pdf(file_path)
    elif extension == ".docx":
        return extract_docx(file_path)    
    elif extension in [".txt", ".md"]:
        return extract_txt(file_path) 
    raise ValueError(f"Unsupported file type: {extension}. Supported types are: .pdf, .docx, .txt, .md")

def load_docuents(dir_path : str | Path) -> list[dict]:
  dir_path = Path(dir_path)
  if not dir_path.exists():
    raise FileNotFoundError(f"Data Directory Not Found: {dir_path}")
  if not dir_path.is_dir():
    raise ValueError(f"Given path is not of a directory: {dir_path}")
  
  all_files=[]
  for file_path in dir_path.rglob("*"):
    if not file_path.is_file():
      continue
    try:
      items = load_document(file_path)
      all_files.extend(items)

    except ValueError as exc:
      print(f"Skipping {file_path}: {exc}")
  return all_files