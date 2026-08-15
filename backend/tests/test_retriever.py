import unittest

from app.ai.embeddings import create_embedding
from app.ai.retriever import find_relevant_chunks


class TestRetriever(unittest.TestCase):

    def test_find_relevant_chunks_returns_text_list(self):
        text = "VPN connection not working"

        # 1. Generate query embedding
        embedding = create_embedding(text)
        self.assertIsNotNone(embedding, "Embedding generation failed.")

        # 2. Call your retriever function
        chunks = find_relevant_chunks(embedding, top_k=3)

        print("\n===== RETRIEVED CHUNKS =====")
        print(chunks)

        # 3. Assertions
        self.assertIsInstance(
            chunks, list, "retriever should return a list of strings."
        )
        self.assertTrue(
            len(chunks) > 0,
            "find_relevant_chunks returned an empty list. Verify metadata parsing.",
        )
        self.assertIsInstance(
            chunks[0], str, "Elements in returned chunks must be strings."
        )
        self.assertTrue(len(chunks[0].strip()) > 0, "Top chunk text is empty or blank.")


if __name__ == "__main__":
    unittest.main()
