from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_item(
    item: dict,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[dict]:

    if item["type"] == "text":
        return chunk_text_item(item, chunk_size, chunk_overlap)
    elif item["type"] == "image":
        return process_image_item(item)
    elif item["type"] == "table":
        return chunk_table_item(item)
    else:
        raise ValueError(f"Unsupported document type: {item['type']}")

def chunk_text_item(
    item: dict,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[dict]:

    text = item["text"].strip()

    if not text:
        return []

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
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

    texts = splitter.split_text(text)

    chunks = []

    for chunk_index, chunk_text in enumerate(texts, start=1):
        chunks.append(
            {
                **item,
                "type": "text",
                "text": chunk_text,
                "chunk_index": chunk_index,
            }
        )

    return [
        {
            "source": item["source"],
            "source_path": item.get("source_path"),
            "document_id": item.get("document_id"),
            "type": "text",
            "text": chunk,
            "page": item.get("page"),
        }
        for chunk in chunks
        if chunk.strip()
    ]

def process_image_item(
    item: dict,
    chunk_size: int = 1000,
) -> list[dict]:
    # Placeholder for image processing logic
    return [item]

def chunk_table_item(
    item: dict,
    chunk_size: int = 1000,
) -> list[dict]:

    table = item["table"]
    if not table:
        return []

    #First row is the header
    header = table[0]
    rows = table[1:]
    chunks = []
    current_rows = []

    for row in rows:
        current_rows.append(row)
        table_text= _table_to_text(header, current_rows)
        if len(table_text) >= chunk_size:
            # Keep the current row for the next chunk
            current_rows.pop()

            if current_rows:
                chunks.append(
                    _create_table_chunk(
                        item,
                        header,
                        current_rows,
                        len(chunks) + 1,
                    )
                )

            current_rows = [row]

    if current_rows:
        chunks.append(
            _create_table_chunk(
                item,
                header,
                current_rows,
                len(chunks) + 1,
            )
        )

    return chunks

def _table_to_text(
    header: list,
    rows: list[list],
) -> str:

    lines = [
        " | ".join(
            str(cell).strip()
            for cell in header
        )
    ]

    for row in rows:
        lines.append(
            " | ".join(
                str(cell).strip()
                for cell in row
            )
        )

    return "\n".join(lines)


def _create_table_chunk(
    item: dict,
    header: list,
    rows: list[list],
    chunk_id: int,
) -> dict:

    table_text = _table_to_text(header, rows)

    return {
        "source": item["source"],
        "source_path": item.get("source_path"),
        "document_id": item.get("document_id"),
        "type": "table",
        "text": table_text,
        "table": [header, *rows],
        "page": item.get("page"),
        "table_index": item.get("table_index"),
        "chunk_id": chunk_id,
    }

