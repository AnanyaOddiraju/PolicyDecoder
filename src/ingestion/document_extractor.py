from pathlib import Path
from docx import Document
import fitz  # PyMuPDF
import pdfplumber


def extract_txt(file_path: str) -> list[dict]:
    path = Path(file_path)

    text = path.read_text(encoding="utf-8")

    return [
        {
            "type": "text",
            "text": text,
            "page": None,
            "source": path.name,
        }
    ]


def extract_pdf(file_path: str) -> list[dict]:
    path = Path(file_path)

    documents = []

    # -------------------------
    # Text + Images
    # -------------------------
    pdf = fitz.open(file_path)

    for page_number, page in enumerate(pdf, start=1):

        # Extract text
        text = page.get_text()

        if text.strip():
            documents.append(
                {
                    "type": "text",
                    "text": text,
                    "page": page_number,
                    "source": path.name,
                }
            )

        # Extract images
        images = page.get_images(full=True)

        for image_index, image in enumerate(images, start=1):

            xref = image[0]

            image_data = pdf.extract_image(xref)

            documents.append(
                {
                    "type": "image",
                    "image": image_data["image"],
                    "image_ext": image_data["ext"],
                    "page": page_number,
                    "image_index": image_index,
                    "source": path.name,
                }
            )

    pdf.close()

    # -------------------------
    # Tables
    # -------------------------
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for table_index, table in enumerate(tables, start=1):
                if table:
                    documents.append(
                        {
                            "type": "table",
                            "table": table,
                            "page": page_number,
                            "table_index": table_index,
                            "source": path.name,
                        }
                    )

    return documents


def extract_docx(file_path: str) -> list[dict]:
    path = Path(file_path)

    doc = Document(file_path)

    text = "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
        if paragraph.text.strip()
    )

    return [
        {
            "type": "text",
            "text": text,
            "page": None,
            "source": path.name,
        }
    ]