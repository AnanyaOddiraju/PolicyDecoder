def chunk_image_item(item: dict) -> list[dict]:
    """
    Treat each extracted image as one retrieval unit.

    Actual multimodal embedding will happen later.
    """

    return [
        {
            **item,
            "type": "image",
            "chunk_index": 1,
        }
    ]