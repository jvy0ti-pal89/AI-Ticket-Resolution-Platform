import unittest

from app.ai.llm import generate_structured_response


class TestLLM(unittest.TestCase):
    def test_generate_structured_response_hardware(self):
        title = "Laptop overheating"
        description = "Laptop becomes very hot after 15 minutes."
        result = generate_structured_response(title, description, [])

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("category"), "Hardware")
        self.assertEqual(result.get("priority"), "Medium")
        self.assertIn("Laptop overheating", result.get("summary", ""))


if __name__ == "__main__":
    unittest.main()
