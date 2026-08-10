import os
from docling.document_converter import DocumentConverter


class ParserService:
    def __init__(self):
        # Initialize the standard Docling converter for v2.x
        self.converter = DocumentConverter()

    def parse_document(self, file_path: str) -> str:
        """Parses PDFs via Docling or reads .txt files directly."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Direct read for plain text files
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        # Parse PDFs with Docling
        result = self.converter.convert(file_path)
        return result.document.export_to_markdown()


# Convenience module-level wrapper
_PARSER = ParserService()


def parse_document(file_path: str) -> str:
    return _PARSER.parse_document(file_path)
