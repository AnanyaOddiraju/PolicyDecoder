from pathlib import Path
from src.ingestion.document_extractor import extract_docx, extract_txt,extract_pdf

def load_document(dir_path: str | Path) -> list[Path]:
   
    file_path = Path(dir_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Data directory not found: {file_path}")

    extension = file_path.suffix.lower()

    if extension ==".pdf":
        return extract_pdf(file_path)
    elif extension == ".docx":
        return extract_docx(file_path)    
    elif extension in [".txt", ".md"]:
        return extract_txt(file_path) 
    raise ValueError(f"Unsupported file type: {extension}. Supported types are: .pdf, .docx, .doc, .txt, .md")
   
    # files = []

    # for file_path in data_path.rglob("*"):
    #     if not file_path.is_file():
    #         continue

    #     extension = file_path.suffix.lower()
    #     extracted_file= {}
        
    #     if extension == ".docx":
    #         extracted_file= extract_docx(file_path)
    #     elif extension == ".txt":
    #         extracted_file=  extract_txt(file_path)
    #     elif extension == ".pdf":
    #         extracted_file=  extract_pdf(file_path)
        
    #     files.extend(extracted_file)

    # return files


    