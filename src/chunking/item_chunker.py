from src.chunking.text_chunker import chunk_text_item
from src.chunking.table_chunker import chunk_table_item
from src.chunking.image_chunker import chunk_image_item


def chunk_item(
    item: dict,
    chunk_size: int = 500,
    chunk_overlap: int = 75,
) -> list[dict]:

    item_type = item["type"]

    if item_type == "text":
        return chunk_text_item(
            item,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    elif item_type == "table":
        return chunk_table_item(
            item,
            chunk_size=chunk_size,
        )

    elif item_type == "image":
        return chunk_image_item(item)

    else:
        raise ValueError(
            f"Unsupported extracted item type: {item_type}"
        )