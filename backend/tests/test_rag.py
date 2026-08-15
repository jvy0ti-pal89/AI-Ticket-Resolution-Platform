import unittest

from app.ai.embeddings import create_embedding
from app.ai.vector_store import query_vectors


class TestRAG(unittest.TestCase):

    def test_vector_store_retrieval(self):
        text = "VPN connection not working"

        # Generate query embedding
        embedding = create_embedding(text)
        self.assertIsNotNone(embedding, "Embedding generation returned None.")

        # Query Pinecone directly
        results = query_vectors(embedding, top_k=3)

        print("\n===== RAW PINECONE RESULTS =====")
        print(results)

        # Handle both dict and object response structures safely
        matches = (
            results.get("matches", [])
            if isinstance(results, dict)
            else getattr(results, "matches", [])
        )

        # Assertions
        self.assertIsInstance(
            matches, list, "Pinecone response matches should be a list."
        )
        self.assertTrue(
            len(matches) > 0, "Pinecone returned 0 matches. Verify index is populated."
        )

        # Inspect top match metadata
        first_match = matches[0]
        metadata = (
            first_match.get("metadata")
            if isinstance(first_match, dict)
            else getattr(first_match, "metadata", None)
        )

        self.assertIsNotNone(metadata, "First match has no metadata.")

        chunk_text = metadata.get("chunk_text") or metadata.get("text_preview")
        self.assertIsNotNone(
            chunk_text, "Metadata is missing 'chunk_text' or 'text_preview'."
        )


if __name__ == "__main__":
    unittest.main()