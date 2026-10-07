import tiktoken


def _row_to_text(row: list) -> str:
    return " | ".join(
        str(cell).strip() if cell is not None else ""
        for cell in row
    )


def _create_table_text(
    header: list,
    rows: list[list],
) -> str:

    lines = [
        _row_to_text(header),
        "-" * 40,
    ]

    lines.extend(
        _row_to_text(row)
        for row in rows
    )

    return "\n".join(lines)


def chunk_table_item(
    item: dict,
    chunk_size: int = 500,
) -> list[dict]:

    table = item["table"]

    if not table:
        return []

    header = table[0]
    rows = table[1:]

    # Use tiktoken directly for token counting.
    tokenizer = tiktoken.get_encoding("cl100k_base")

    if not rows:
        table_text = _create_table_text(header, [])

        return [
            {
                **item,
                "type": "table",
                "text": table_text,
                "chunk_index": 1,
            }
        ]

    chunks = []
    current_rows = []

    for row in rows:

        candidate_rows = current_rows + [row]

        candidate_text = _create_table_text(
            header,
            candidate_rows,
        )

        candidate_tokens = len(
            tokenizer.encode(candidate_text)
        )

        if candidate_tokens > chunk_size and current_rows:

            table_text = _create_table_text(
                header,
                current_rows,
            )

            chunks.append(
                {
                    **item,
                    "type": "table",
                    "text": table_text,
                    "chunk_index": len(chunks) + 1,
                }
            )

            # The row that caused the overflow
            # becomes the first row of the next chunk.
            current_rows = [row]

        else:
            current_rows.append(row)

    # Add remaining rows.
    if current_rows:

        table_text = _create_table_text(
            header,
            current_rows,
        )

        chunks.append(
            {
                **item,
                "type": "table",
                "text": table_text,
                "chunk_index": len(chunks) + 1,
            }
        )

    return chunks