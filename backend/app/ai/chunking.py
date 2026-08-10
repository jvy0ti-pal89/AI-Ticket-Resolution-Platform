from typing import List


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
    """Split `text` into chunks using a RecursiveCharacterTextSplitter-like strategy.

    Falls back to a simple sliding-window splitter if LangChain is not available.
    """
    try:
        # Prefer langchain splitter when available
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        return splitter.split_text(text)
    except Exception:
        # Simple fallback splitter: split on sentences and accumulate
        import re

        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = []
        current = []
        current_len = 0
        for s in sentences:
            slen = len(s)
            if current_len + slen <= chunk_size or not current:
                current.append(s)
                current_len += slen
            else:
                chunks.append(" ".join(current))
                # start new chunk with overlap
                if chunk_overlap > 0:
                    # keep last overlap chars from the joined current
                    overlap_text = (" ".join(current))[-chunk_overlap:]
                    current = [overlap_text, s]
                    current_len = len(overlap_text) + slen
                else:
                    current = [s]
                    current_len = slen
        if current:
            chunks.append(" ".join(current))
        return chunks
