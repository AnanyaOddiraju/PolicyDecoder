from pathlib import Path
from docx import Document
import pymupdf
import pdfplumber

def _common_metadata(path: Path) -> dict:
    #Common metadata for every extracted document
    return {
        "source": path.name,
        "document_id": path.stem,
    }


def extract_txt(file_path: str | Path) -> list[dict]:
    path = Path(file_path)

    text = path.read_text(encoding="utf-8")

    if not text.strip():
        return []
    
    metadata = _common_metadata(Path)  
    return [
        {
            **metadata,
            "type": "text",
            "text": text.strip(),
            "page": None
        }
    ]


def extract_pdf(file_path: str | Path) -> list[dict]:
    #From pdf's we extract text, images, tables
    path = Path(file_path)
    extracted_items= []

    # Text + Images using PyMuPDF
    pdf = pymupdf.open(file_path)

    try:
      for page_number, page in enumerate(pdf, start=1):
        
        metadata= _common_metadata(path)
        # Extract text
        text = page.get_text("text").strip()

        if text:
            extracted_items.append(
                {
                    **metadata,
                    "type": "text",
                    "text": text,
                    "page": page_number,
                }
            )

        # Extract images
        images = page.get_images(full=True)

        for image_index, image in enumerate(images, start=1):

            xref = image[0]

            try:
              image_data = pdf.extract_image(xref)

              extracted_items.append(
                {
                    **metadata,
                    "type": "image",
                    "image": image_data["image"],
                    "image_ext": image_data["ext"],
                    "page": page_number,
                    "image_index": image_index,
                }
              )
            except Exception as exc:
              print(f"Could not extract image"
                    f"{image_index} from page {page_number} :{exc}"
              )
    finally:
      pdf.close()

    # Tables using pdfplumber
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for table_index, table in enumerate(tables, start=1):
                if not table:
                  continue
                
                #Removing empty rows
                cleaned_table = [
                  row 
                  for row in table
                  if row and any(cell and str(cell).strip() for cell in row)
                ]
                if not cleaned_table:
                  continue
                metadata= _common_metadata(path)
                
                extracted_items.append(
                {
                  **metadata,
                  "type": "table",
                  "table": table,
                  "page": page_number,
                  "table_index": table_index,
                }
                )

    return extracted_items


def extract_docx(file_path: str | Path) -> list[dict]:
    path = Path(file_path)

    doc = Document(file_path)

    metadata = _common_metadata(path)
    extracted_items=[]
    text = "\n".join(
        paragraph.text.strip()
        for paragraph in doc.paragraphs
        if paragraph.text.strip()
    )

    if text:
        extracted_items.append(
            {
                **metadata,
                "type": "text",
                "text": text,
                "page": None,
            }
        )

    #Tables
    for table_index, table in enumerate(doc.tables, start=1):

        rows = []

        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]

            if any(cells):
                rows.append(cells)

        if rows:
            extracted_items.append(
                {
                    **metadata,
                    "type": "table",
                    "table": rows,
                    "page": None,
                    "table_index": table_index,
                }
            )
    return extracted_items
