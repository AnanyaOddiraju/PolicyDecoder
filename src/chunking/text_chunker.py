from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_document(
    document: dict,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[dict]:

    text = document["text"].strip()

    if not text:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_text(text)

    return [
        {
            "source": document["source"],
            "text": chunk,
            "page": document.get("page"),
        }
        for chunk in chunks
        if chunk.strip()
    ]