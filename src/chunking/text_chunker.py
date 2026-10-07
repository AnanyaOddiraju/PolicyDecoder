from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text_item(
    item: dict,
    chunk_size: int = 500,
    chunk_overlap: int = 75,
) -> list[dict]:
    """
    Split a text extracted_item into token-aware chunks.

    The splitter uses the tokenizer associated with the embedding/LLM
    model rather than raw character count.
    """

    text = item["text"].strip()

    if not text:
        return []

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",   # paragraph
            "\n",     # line
            ". ",     # sentence
            " ",      # word
            "",       # character fallback
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

    return chunks