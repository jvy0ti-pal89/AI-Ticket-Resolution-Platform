import unittest


from app.services.rag_service import create_ticket_resolution


class TestRAGService(unittest.TestCase):

    def test_create_ticket_resolution_returns_grounded_response(self):
        title = "vpn resolution guide"
        description = "Need the vpn resolution guide steps to fix connection failure."

        # Call full RAG service flow (Embedding -> Pinecone -> Prompt -> Groq)
        result = create_ticket_resolution(title, description)

        print("\n===== FULL RAG PIPELINE RESULT =====")
        print(result)

        # Assertions
        self.assertIsInstance(result, dict, "RAG response must be a dictionary.")
        self.assertIn("category", result, "Missing 'category' in LLM response.")
        self.assertIn("priority", result, "Missing 'priority' in LLM response.")
        self.assertIn("summary", result, "Missing 'summary' in LLM response.")
        self.assertIn("resolution", result, "Missing 'resolution' in LLM response.")

        resolution_text = result.get("resolution", "").lower()
        self.assertTrue(
            len(resolution_text) > 0, "Resolution returned by LLM is empty."
        )

        # Ensure response isn't using the generic fallback text
        self.assertNotIn(
            "investigate the issue",
            resolution_text,
            "RAG returned generic fallback instead of LLM generated output.",
        )


if __name__ == "__main__":
    unittest.main()
