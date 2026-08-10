from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.services.rag_service import create_ticket_resolution


def enrich_ticket_with_ai(db: Session, ticket: Ticket) -> None:
    """Enrich ticket record with category, priority, summary, grounded resolution, and hand off to review."""
    structured = create_ticket_resolution(ticket.title, ticket.description)

    ticket.category = structured.get("category") or ticket.category or "General"
    ticket.priority = structured.get("priority") or ticket.priority or "Medium"
    ticket.summary = structured.get("summary") or ticket.summary or ticket.title
    ticket.resolution = structured.get("resolution") or ticket.resolution or ""
    ticket.status = "PENDING_REVIEW"
