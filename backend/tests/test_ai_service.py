import unittest

from app.models.ticket import Ticket
from app.services.ai_service import enrich_ticket_with_ai


class TestAIService(unittest.TestCase):
    def test_enrich_ticket_with_ai_sets_fields(self):
        ticket = Ticket(
            title="Laptop overheating",
            description="Laptop becomes very hot after 15 minutes.",
        )
        # db is not used by current implementation, pass None
        enrich_ticket_with_ai(None, ticket)

        self.assertEqual(ticket.category, "Hardware")
        self.assertEqual(ticket.priority, "Medium")
        self.assertTrue(ticket.summary is not None and ticket.summary != "")
        self.assertTrue(ticket.resolution is not None and ticket.resolution != "")


if __name__ == "__main__":
    unittest.main()
